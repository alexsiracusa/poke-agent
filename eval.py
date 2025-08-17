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
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass
import signal
import sys
from icecream import ic
from rich.console import Console
from rich.theme import Theme

# Set up rich console with custom theme (emoji-free, elegant)
custom_theme = Theme({
    "info": "bold cyan",
    "warning": "bold yellow",
    "error": "bold red",
    "success": "bold green"
})
console = Console(theme=custom_theme, emoji=False)

# Metamon imports - use direct import since it's installed as part of the package
from metamon.env import QueueOnLocalLadder, get_metamon_teams
from metamon.interface import DefaultObservationSpace, DefaultShapedReward, DefaultActionSpace
from metamon.baselines import ALL_BASELINES

# Poke-env imports for ladder play
from poke_env import AccountConfiguration, LocalhostServerConfiguration

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
    print("Warning: Pretrained models not available. Install amago for pretrained model support.")

@dataclass
class AgentConfig:
    name: str
    agent_class: Any
    username: str
    battles_completed: int = 0
    is_running: bool = False
    env: Any = None

class TournamentManager:
    def __init__(self, battle_format: str, target_battles: int):
        self.battle_format = battle_format
        self.target_battles = target_battles
        self.agents: List[AgentConfig] = []
        self.running = True
        
        # Setup metamon components
        self.team_set = get_metamon_teams(battle_format, "competitive")
        self.obs_space = DefaultObservationSpace()
        self.action_space = DefaultActionSpace()
        self.reward_fn = DefaultShapedReward()
        
        # Setup signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
    
    def _signal_handler(self, sig, frame):
        console.print("\n[warning]Shutting down gracefully...[/]", style="warning")
        self.running = False
        # Force stop all agents
        for agent_config in self.agents:
            agent_config.is_running = False
            if agent_config.env and hasattr(agent_config.env, 'close'):
                try:
                    agent_config.env.close()
                except Exception:
                    pass
        # Force exit more aggressively
        os._exit(0)
    
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
        assert isinstance(available_agents, dict), "Available agents should be a dict!"
        if agent_name not in available_agents:
            console.print(f"[error]Agent '{agent_name}' not available.[/]", style="error")
            console.print(f"[info]Available agents: {list(available_agents.keys())}[/]", style="info")
            return False
        username = f"e_{agent_name[:10]}_{len(self.agents)+1:02d}"
        agent_config = AgentConfig(
            name=agent_name,
            agent_class=available_agents[agent_name],
            username=username
        )
        self.agents.append(agent_config)
        console.print(f"[success]Added agent: {agent_name} as {username}[/]", style="success")
        return True
    
    def _create_agent_env(self, agent_config: AgentConfig):
        """Create QueueOnLocalLadder environment for ANY agent type - baselines AND pretrained"""
        try:
            from metamon.env import QueueOnLocalLadder
            
            # EVERYONE uses QueueOnLocalLadder - no exceptions!
            # Use the CORRECT parameter names from the actual signature
            env = QueueOnLocalLadder(
                battle_format=self.battle_format,
                num_battles=self.target_battles,
                observation_space=self.obs_space,
                action_space=self.action_space,
                reward_function=self.reward_fn,
                player_team_set=self.team_set,  # Correct parameter name!
                player_username=agent_config.username,  # Correct parameter name!
                start_timer_on_battle_start=True,
                print_battle_bar=True,
            )
            
            console.print(f"[success]Created QueueOnLocalLadder for {agent_config.name}[/]")
            return env
            
        except Exception as e:
            console.print(f"[error]Error creating env for {agent_config.name}: {e}[/]")
            return None

    def _run_agent(self, agent_config: AgentConfig):
        """Run ANY agent type using QueueOnLocalLadder"""
        agent_config.is_running = True
        
        # Create QueueOnLocalLadder environment
        env = self._create_agent_env(agent_config)
        if env is None:
            agent_config.is_running = False
            return
            
        agent_config.env = env
        
        try:
            console.print(f"[info]Starting {agent_config.name} on local ladder...[/]")
            
            # Run battles using the environment
            battles_completed = 0
            while battles_completed < self.target_battles and self.running and agent_config.is_running:
                try:
                    # Reset environment and get initial observation
                    obs, info = env.reset()
                    done = False
                    
                    while not done and self.running and agent_config.is_running:
                        try:
                            if agent_config.name in ALL_BASELINES:
                                # For heuristic baselines, implement their logic here
                                action = self._get_baseline_action(agent_config.name, obs, info)
                            else:
                                # For pretrained models, load model and get action
                                action = self._get_pretrained_action(agent_config.name, obs, info)
                            
                            obs, reward, terminated, truncated, info = env.step(action)
                            done = terminated or truncated
                        except Exception as e:
                            console.print(f"[error]Step error for {agent_config.name}: {e}[/]")
                            # Try to continue with next battle instead of crashing
                            break
                    
                    battles_completed += 1
                    agent_config.battles_completed = battles_completed
                    console.print(f"[info]{agent_config.name}: {battles_completed}/{self.target_battles} battles[/]")
                    
                except Exception as e:
                    console.print(f"[error]Battle error for {agent_config.name}: {e}[/]")
                    # Try to continue instead of completely stopping
                    battles_completed += 1  # Count as completed to avoid infinite loop
                    agent_config.battles_completed = battles_completed
                    continue
                    
            console.print(f"[success]{agent_config.name} completed {agent_config.battles_completed} battles[/]")
            
        except KeyboardInterrupt:
            console.print(f"[warning]{agent_config.name} interrupted[/]")
        except Exception as e:
            console.print(f"[error]Error running agent {agent_config.name}: {e}[/]")
        finally:
            agent_config.is_running = False
            if env and hasattr(env, 'close'):
                try:
                    env.close()
                except Exception:
                    pass

    def _get_baseline_action(self, baseline_name: str, obs, info):
        """Get action from heuristic baseline logic"""
        # Use the action space's sample method correctly
        return self.action_space.sample()

    def _get_pretrained_action(self, model_name: str, obs, info):
        """Get action from pretrained model"""
        # TODO: Load and run pretrained model inference
        # For now, placeholder with random action
        console.print(f"[warning]Pretrained model {model_name} not implemented, using random[/]")
        return self.action_space.sample()

    def _gen1_boss_logic(self, obs, info):
        """Simple Gen1BossAI logic"""
        # Implement basic Gen1 AI behavior
        # For now, just random
        return self.action_space.sample()

    def _gym_leader_logic(self, obs, info):
        """Simple GymLeader logic"""
        # Implement GymLeader behavior
        # For now, just random  
        return self.action_space.sample()    
    
    def start_tournament(self):
        """Start all agents in separate threads"""
        if not self.agents:
            console.print("[error]No agents to run![/]", style="error")
            return
        console.print(f"[success]Starting tournament with {len(self.agents)} agents...[/]", style="success")
        console.print(f"[info]Format: {self.battle_format}, Target battles: {self.target_battles}[/]", style="info")
        
        # Start each agent in a separate thread
        threads = []
        for agent_config in self.agents:
            thread = threading.Thread(target=self._run_agent, args=(agent_config,))
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        try:
            # Monitor progress
            self._monitor_progress()
            
            # Wait for all threads to complete with a timeout to check for interruptions
            for thread in threads:
                while thread.is_alive() and self.running:
                    thread.join(timeout=1.0)  # Check every second if we should stop
                    
        except KeyboardInterrupt:
            console.print("\n[warning]Tournament interrupted by user[/]", style="warning")
            self.running = False
            # Force stop all agents
            for agent_config in self.agents:
                agent_config.is_running = False
                if agent_config.env and hasattr(agent_config.env, 'close'):
                    try:
                        agent_config.env.close()
                    except Exception:
                        pass
        
        # Final cleanup
        for agent_config in self.agents:
            agent_config.is_running = False
            if agent_config.env and hasattr(agent_config.env, 'close'):
                try:
                    agent_config.env.close()
                except Exception:
                    pass
        
        console.print("\n[success]Tournament completed![/]", style="success")
        self._print_final_results()
    
    def _monitor_progress(self):
        """Monitor and display tournament progress"""
        timeout_counter = 0
        max_timeout = 600  # 10 minutes of no progress before giving up
        
        while self.running and not self._all_agents_complete():
            self._print_progress()
            
            # Check if any agent is still making progress
            any_running = any(agent.is_running for agent in self.agents)
            if not any_running:
                console.print("[warning]No agents are running, stopping tournament[/]", style="warning")
                break
            
            # Sleep in smaller chunks to be more responsive to interruptions
            for _ in range(30):  # 30 seconds total, checking every second
                if not self.running:
                    break
                time.sleep(1)
                timeout_counter += 1
                
                # Check timeout
                if timeout_counter > max_timeout:
                    console.print("[warning]Tournament timeout reached, stopping[/]", style="warning")
                    self.running = False
                    break
    
    def _print_progress(self):
        """Print current tournament progress"""
        console.print(f"\n[info]Tournament Progress ({self.battle_format}):[/]", style="info")
        total_battles = 0
        total_target = len(self.agents) * self.target_battles
        for agent_config in self.agents:
            # Update battle count from player if available
            if agent_config.env and hasattr(agent_config.env, 'n_finished_battles'):
                agent_config.battles_completed = agent_config.env.n_finished_battles
            
            status = "RUNNING" if agent_config.is_running else "STOPPED"
            console.print(f"{agent_config.username:20}: {agent_config.battles_completed:3d}/{self.target_battles} battles [{status}]", style="info")
            total_battles += agent_config.battles_completed
        console.print(f"\n[info]Total: {total_battles}/{total_target} battles complete[/]", style="info")
        if total_target > 0:
            percentage = (total_battles / total_target) * 100
            console.print(f"[info]Progress: {percentage:.1f}%[/]", style="info")
    
    def _all_agents_complete(self) -> bool:
        """Check if all agents have completed their target battles"""
        return all(agent.battles_completed >= self.target_battles for agent in self.agents)
    
    def _print_final_results(self):
        """Print final tournament results"""
        console.print("\n" + "="*50, style="success")
        console.print("[success]TOURNAMENT COMPLETE[/]", style="success")
        console.print("="*50, style="success")
        for agent_config in self.agents:
            console.print(f"{agent_config.name:20}: {agent_config.battles_completed}/{self.target_battles} battles", style="info")
        console.print(f"\n[info]Check Pokemon Showdown ladder for full results:[/]", style="info")
        console.print(f"http://localhost:8000/ladder/{self.battle_format}", style="info")

@click.command()
@click.option('--agents', required=False, 
              help='Comma-separated list of agent names')
@click.option('--battles', default=50, 
              help='Number of battles per agent')
@click.option('--format', 'battle_format', default='gen1ou',
              help='Battle format (gen1ou, gen2ou, etc.)')
@click.option('--list-agents', is_flag=True,
              help='List all available agents')
def main(agents, battles, battle_format, list_agents):
    """
    Run a Pokemon Showdown tournament with multiple metamon agents.
    
    Examples:
        python eval.py --agents "GymLeader,RandomBaseline" --battles 20 --format gen1ou
        python eval.py --agents "SyntheticRLV2,LargeRL" --battles 50 --format gen1ou
        python eval.py --list-agents
    """
    
    manager = TournamentManager(battle_format, battles)
    
    if list_agents:
        available_agents = manager.get_all_available_agents()
        console.print("[info]Available agents:[/]")
        heuristics = [name for name in available_agents.keys() if name in ALL_BASELINES]
        pretrained = [name for name in available_agents.keys() if name not in ALL_BASELINES]
        if heuristics:
            console.print("\n[info]Heuristic Baselines:[/]")
            for agent in sorted(heuristics):
                console.print(f"  - {agent}", style="info")
        if pretrained:
            console.print("\n[info]Pretrained Models:[/]")
            for agent in sorted(pretrained):
                console.print(f"  - {agent}", style="info")
        if not PRETRAINED_AVAILABLE:
            console.print("\n[warning]Note: Install amago to use pretrained models[/]", style="warning")
        return
    
    # Check if agents parameter is provided when not listing agents
    if not agents:
        console.print("[error]--agents option is required when not using --list-agents[/]", style="error")
        sys.exit(1)
    
    # Parse agent list
    agent_names = [name.strip() for name in agents.split(',')]
    
    # Add agents to tournament
    for agent_name in agent_names:
        assert isinstance(agent_name, str) and agent_name, "Agent name must be a non-empty string!"
        if not manager.add_agent(agent_name):
            sys.exit(1)
    
    # Start tournament
    try:
        manager.start_tournament()
    except KeyboardInterrupt:
        console.print("\n[warning]Tournament interrupted by user[/]", style="warning")
        # Force cleanup and exit
        manager.running = False
        for agent_config in manager.agents:
            agent_config.is_running = False
            if agent_config.env and hasattr(agent_config.env, 'close'):
                try:
                    agent_config.env.close()
                except Exception:
                    pass
        os._exit(0)
    except Exception as e:
        console.print(f"\n[error]Unexpected error: {e}[/]", style="error")
        os._exit(1)

if __name__ == '__main__':
    main()