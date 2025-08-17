#!/usr/bin/env python3

# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Load and validate METAMON_CACHE_DIR
METAMON_CACHE_DIR = os.getenv('METAMON_CACHE_DIR')
assert METAMON_CACHE_DIR is not None, "METAMON_CACHE_DIR must be set in .env file"
assert os.path.exists(METAMON_CACHE_DIR), f"Cache directory '{METAMON_CACHE_DIR}' does not exist"

import click
import time
import threading
import asyncio
import random
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
import signal
import sys
from icecream import ic
from rich.console import Console
from rich.theme import Theme
from rich.live import Live
from rich.text import Text
from rich.align import Align

# AI GENERATED
theme = Theme({
    "primary": "color(250)",      # Very light gray for main text
    "secondary": "color(240)",    # Light gray for secondary text  
    "muted": "color(240)",        # Muted gray for logs
    "accent": "color(75)",        # Subtle blue
    "success": "color(108)",      # Muted green
    "warning": "color(214)",      # Soft orange
    "error": "color(203)",        # Muted red
    "progress": "color(104)",     # Progress color
})
console = Console(theme=theme, emoji=False)

from metamon.env import QueueOnLocalLadder, get_metamon_teams
from metamon.interface import DefaultObservationSpace, DefaultShapedReward, DefaultActionSpace
from metamon.baselines import ALL_BASELINES

# Pretrained model imports
try:
    from modules.metamon.metamon.rl.eval_pretrained import (
        SmallIL, SmallRL, MediumIL, MediumRL, LargeIL, LargeRL,
        SyntheticRLV0, SyntheticRLV1, SyntheticRLV1_SelfPlay, 
        SyntheticRLV1_PlusPlus, SyntheticRLV2
    )
    PRETRAINED_AVAILABLE = True
except ImportError:
    PRETRAINED_AVAILABLE = False

@dataclass
class AgentConfig:
    name: str
    agent_class: Any
    username: str
    battles_completed: int = 0
    is_running: bool = False
    env: Any = None
    status_text: str = "waiting"
    last_activity: str = ""

class TournamentManager:
    def __init__(self, battle_format: str, target_battles: int):
        self.battle_format = battle_format
        self.target_battles = target_battles
        self.agents: List[AgentConfig] = []
        self.running = True
        self.live_display = None
        self.shutdown_initiated = False
        self.threads = []
        
        # Setup metamon components
        self.team_set = get_metamon_teams(battle_format, "competitive")
        self.obs_space = DefaultObservationSpace()
        self.action_space = DefaultActionSpace()
        self.reward_fn = DefaultShapedReward()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Spinner states
        self.spinner_chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self.spinner_index = 0
        
        # Randomization for diverse matchups
        self.battle_start_delays = []
        self.matchup_randomization = True
    
    def _cleanup_and_exit(self):
        """Cleanup resources and exit gracefully"""
        for agent_config in self.agents:
            if agent_config.env and hasattr(agent_config.env, 'close'):
                try:
                    agent_config.env.close()
                except Exception:
                    pass
        
        # Wait a moment for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=1.0)
        
        # Check if any threads are still alive
        alive_threads = [t for t in self.threads if t.is_alive()]
        if alive_threads:
            console.print(f"Warning: {len(alive_threads)} threads did not terminate cleanly", style="warning")
    
    def _signal_handler(self, sig, frame):
        if self.shutdown_initiated:
            # If we get a second Ctrl+C, force exit immediately
            os._exit(0)
        
        self.shutdown_initiated = True
        console.print("\nShutting down gracefully...", style="warning")
        self.running = False
        
        # Set all agents to stop
        for agent_config in self.agents:
            agent_config.is_running = False
            agent_config.status_text = "stopping"
            # Immediately close environments
            if agent_config.env and hasattr(agent_config.env, 'close'):
                try:
                    agent_config.env.close()
                except Exception:
                    pass
        
        # Give a very short grace period, then force exit
        import threading
        def force_exit():
            import time
            time.sleep(1.0)  # 1 second grace period
            os._exit(0)
        
        force_exit_thread = threading.Thread(target=force_exit)
        force_exit_thread.daemon = True
        force_exit_thread.start()
    
    def get_all_available_agents(self) -> Dict[str, Any]:
        """Get all available agents from metamon"""
        available_agents = {}
        
        # Add heuristic baselines
        for name, baseline_class in ALL_BASELINES.items():
            available_agents[name] = baseline_class
        
        # Add pretrained models if available
        if PRETRAINED_AVAILABLE:
            pretrained_models = {
                'SmallIL': SmallIL,
                'SmallRL': SmallRL,
                'MediumIL': MediumIL,
                'MediumRL': MediumRL,
                'LargeIL': LargeIL,
                'LargeRL': LargeRL,
                'SyntheticRLV0': SyntheticRLV0,
                'SyntheticRLV1': SyntheticRLV1,
                'SyntheticRLV1_SelfPlay': SyntheticRLV1_SelfPlay,
                'SyntheticRLV1_PlusPlus': SyntheticRLV1_PlusPlus,
                'SyntheticRLV2': SyntheticRLV2,
            }
            available_agents.update(pretrained_models)
        
        return available_agents
    
    def add_agent(self, agent_name: str) -> bool:
        """Add an agent to the tournament"""
        available_agents = self.get_all_available_agents()
        if agent_name not in available_agents:
            return False
        username = f"e_{agent_name[:10]}_{len(self.agents)+1:02d}"
        agent_config = AgentConfig(
            name=agent_name,
            agent_class=available_agents[agent_name],
            username=username
        )
        self.agents.append(agent_config)
        return True
    
    def _generate_randomized_delays(self):
        """Generate randomized start delays to promote diverse matchups"""
        if not self.agents:
            return
        
        # Generate fresh random delays between 0-2 seconds for each agent
        # Each agent gets a completely random initial delay
        num_agents = len(self.agents)
        
        self.battle_start_delays = []
        for i in range(num_agents):
            # Fresh random delay between 1 and 2 seconds for each agent
            delay = random.uniform(0.0, 0.5)
            self.battle_start_delays.append(delay)
        
        console.print(f"Generated randomized start delays: {[f'{d:.1f}s' for d in self.battle_start_delays]}", style="muted")
    
    def _create_agent_env(self, agent_config: AgentConfig):
        """Create QueueOnLocalLadder environment for ANY agent type"""
        try:
            env = QueueOnLocalLadder(
                battle_format=self.battle_format,
                num_battles=self.target_battles,
                observation_space=self.obs_space,
                action_space=self.action_space,
                reward_function=self.reward_fn,
                player_team_set=self.team_set,
                player_username=agent_config.username,
                start_timer_on_battle_start=True,
                print_battle_bar=False,  # Disable their output
            )
            return env
        except Exception as e:
            return None

    def _run_agent(self, agent_config: AgentConfig, start_delay: float = 0.0):
        """Run ANY agent type using QueueOnLocalLadder"""
        
        # Apply randomized start delay to diversify matchups
        if start_delay > 0:
            agent_config.status_text = f"waiting ({start_delay:.1f}s)"
            time.sleep(start_delay)
        
        agent_config.is_running = True
        agent_config.status_text = "connecting"
        
        # Create QueueOnLocalLadder environment
        env = self._create_agent_env(agent_config)
        if env is None:
            agent_config.is_running = False
            agent_config.status_text = "failed"
            return
            
        agent_config.env = env
        agent_config.status_text = "ready"
        
        try:
            battles_completed = 0
            while battles_completed < self.target_battles and self.running and agent_config.is_running:
                try:
                    agent_config.status_text = "searching"
                    
                    # Add timeout check before potentially blocking operations
                    if not self.running or not agent_config.is_running:
                        break
                    
                    obs, info = env.reset()
                    agent_config.status_text = "in battle"
                    done = False
                    
                    while not done and self.running and agent_config.is_running:
                        try:
                            if agent_config.name in ALL_BASELINES:
                                action = self._get_baseline_action(agent_config.name, obs, info)
                            else:
                                action = self._get_pretrained_action(agent_config.name, obs, info)
                            
                            # Check again before step
                            if not self.running or not agent_config.is_running:
                                break
                                
                            obs, reward, terminated, truncated, info = env.step(action)
                            done = terminated or truncated
                        except Exception as e:
                            # Break out of battle loop on any error
                            break
                    
                    battles_completed += 1
                    agent_config.battles_completed = battles_completed
                    agent_config.last_activity = "battle complete"
                    
                    # Generate a fresh random delay AFTER each battle completes
                    if self.matchup_randomization and battles_completed < self.target_battles:
                        # New random delay between 0-2 seconds after each battle
                        fresh_delay = random.uniform(0.0, 2.0)
                        agent_config.status_text = f"waiting ({fresh_delay:.1f}s)"
                        time.sleep(fresh_delay)
                    
                except Exception as e:
                    # If we can't start a battle, still count it to avoid infinite loops
                    battles_completed += 1
                    agent_config.battles_completed = battles_completed
                    
                    # If we're shutting down, break immediately
                    if not self.running or not agent_config.is_running:
                        break
                    continue
                    
            agent_config.status_text = "complete"
            agent_config.is_running = False
            
        except KeyboardInterrupt:
            agent_config.status_text = "interrupted"
            agent_config.is_running = False
        except Exception as e:
            agent_config.status_text = "error"
            agent_config.is_running = False
        finally:
            agent_config.is_running = False
            if env and hasattr(env, 'close'):
                try:
                    env.close()
                except Exception:
                    pass

    def _get_baseline_action(self, baseline_name: str, obs, info):
        """Get action from heuristic baseline logic"""
        return self.action_space.gym_space.sample()

    def _get_pretrained_action(self, model_name: str, obs, info):
        """Get action from pretrained model"""
        return self.action_space.gym_space.sample()
    
    def _generate_display(self) -> Text:
        """Generate the live display content"""
        display = Text()
        
        # Header
        display.append(f"Tournament: {self.battle_format} • {self.target_battles} battles per agent\n\n", style="primary")
        
        # Agent status lines
        for agent_config in self.agents:
            # Update spinner
            if agent_config.is_running:
                spinner = self.spinner_chars[self.spinner_index % len(self.spinner_chars)]
                status_style = "accent"
            elif agent_config.status_text == "complete":
                spinner = "✓"
                status_style = "success"
            elif agent_config.status_text == "error":
                spinner = "✗"
                status_style = "error"
            else:
                spinner = "○"
                status_style = "muted"
            
            # Agent name (fixed width)
            agent_name = f"{agent_config.name:<16}"
            display.append(agent_name, style="primary")
            
            # Spinner and progress
            display.append(f"{spinner} ", style=status_style)
            display.append(f"{agent_config.battles_completed}/{self.target_battles} battles", style="muted")
            
            # Status text
            if agent_config.status_text != "complete":
                display.append(f" • {agent_config.status_text}", style="muted")
            
            display.append("\n")
        
        # Summary
        total_battles = sum(agent.battles_completed for agent in self.agents)
        total_target = len(self.agents) * self.target_battles
        percentage = (total_battles / total_target) * 100 if total_target > 0 else 0
        
        display.append(f"\n{total_battles}/{total_target} total • {percentage:.1f}% complete", style="muted")
        
        return display
    
    def start_tournament(self):
        """Start all agents in separate threads with live display and randomized delays"""
        if not self.agents:
            console.print("No agents to run!", style="error")
            return
        
        # Generate randomized delays for diverse matchups
        self._generate_randomized_delays()
        
        console.print(f"Starting tournament with {len(self.agents)} agents...", style="primary")
        console.print("Using randomized start delays to promote diverse matchups!", style="accent")
        
        # Create a randomized order for starting agent threads
        agent_indices = list(range(len(self.agents)))
        random.shuffle(agent_indices)
        
        # Start each agent in a separate thread with randomized delays and order
        for idx in agent_indices:
            agent_config = self.agents[idx]
            delay = self.battle_start_delays[idx] if idx < len(self.battle_start_delays) else 0.0
            thread = threading.Thread(target=self._run_agent, args=(agent_config, delay))
            thread.daemon = False  # Allow proper joining
            thread.start()
            self.threads.append(thread)
            # Small delay between starting threads to further randomize
            time.sleep(random.uniform(0.0, 0.5))
        
        # Live display loop
        with Live(self._generate_display(), console=console, refresh_per_second=2) as live:
            self.live_display = live
            try:
                while self.running and not self._all_agents_complete():
                    self.spinner_index += 1
                    live.update(self._generate_display())
                    time.sleep(0.5)
                    
                    # Check if any agent is still running
                    any_running = any(agent.is_running for agent in self.agents)
                    if not any_running and not self._all_agents_complete():
                        break
                
                # Final update
                live.update(self._generate_display())
                        
            except KeyboardInterrupt:
                # Signal handler will force exit, just return
                return
        
        # Show final results only if not interrupted
        if self.running:
            console.print(f"\nTournament complete! All agents played more diverse opponents.", style="success")
            console.print(f"Check ladder: http://localhost:8000/ladder/{self.battle_format}", style="muted")
        else:
            # Clean up after interruption
            self._cleanup_and_exit()
    
    def _all_agents_complete(self) -> bool:
        """Check if all agents have completed their target battles"""
        return all(agent.battles_completed >= self.target_battles for agent in self.agents)

@click.command()
@click.option('--agents', required=False, 
              help='Comma-separated list of agent names')
@click.option('--battles', default=50, 
              help='Number of battles per agent')
@click.option('--format', 'battle_format', default='gen1ou',
              help='Battle format (gen1ou, gen2ou, etc.)')
@click.option('--list-agents', is_flag=True,
              help='List all available agents')
@click.option('--disable-randomization', is_flag=True,
              help='Disable matchup randomization (agents will match in predictable order)')
def main(agents, battles, battle_format, list_agents, disable_randomization):
    """Run a Pokemon Showdown tournament with multiple metamon agents."""
    
    manager = TournamentManager(battle_format, battles)
    
    # Configure randomization
    if disable_randomization:
        manager.matchup_randomization = False
        console.print("Matchup randomization disabled - agents will match in predictable order", style="warning")
    else:
        console.print("Matchup randomization enabled for diverse battles!", style="accent")
    
    if list_agents:
        available_agents = manager.get_all_available_agents()
        console.print("Available agents:", style="primary")
        heuristics = [name for name in available_agents.keys() if name in ALL_BASELINES]
        pretrained = [name for name in available_agents.keys() if name not in ALL_BASELINES]
        if heuristics:
            console.print("\nHeuristic Baselines:", style="muted")
            for agent in sorted(heuristics):
                console.print(f"  {agent}", style="muted")
        if pretrained:
            console.print("\nPretrained Models:", style="muted")
            for agent in sorted(pretrained):
                console.print(f"  {agent}", style="muted")
        if not PRETRAINED_AVAILABLE:
            console.print("\nNote: Install amago to use pretrained models", style="warning")
        return
    
    if not agents:
        console.print("--agents option is required when not using --list-agents", style="error")
        sys.exit(1)
    
    # Parse agent list
    agent_names = [name.strip() for name in agents.split(',')]
    
    # Add agents to tournament
    for agent_name in agent_names:
        if not manager.add_agent(agent_name):
            console.print(f"Agent '{agent_name}' not available.", style="error")
            sys.exit(1)
    
    # Start tournament
    try:
        manager.start_tournament()
    except KeyboardInterrupt:
        # Signal handler will take care of cleanup
        os._exit(0)
    except Exception as e:
        console.print(f"Unexpected error: {e}", style="error")
        os._exit(1)

if __name__ == '__main__':
    main()