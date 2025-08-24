import torch
import torch.nn as nn

class HybridEmbedding(nn.Module):
    def __init__(self, num_embeddings, num_static_features, num_learnable_features, static_features):
        super().__init__()
        assert static_features.shape == (num_embeddings, num_static_features)

        # store fixed part (not learnable)
        self.register_buffer("static_features", static_features)

        # learnable part
        self.learnable = nn.Embedding(num_embeddings, num_learnable_features)

    def forward(self, indices):
        static = self.static_features[indices]                 # (batch, num_static_features)
        learnable = self.learnable(indices)                    # (batch, num_learnable_features)
        return torch.cat([static, learnable], dim=-1)  # (batch, num_static+num_learnable)
