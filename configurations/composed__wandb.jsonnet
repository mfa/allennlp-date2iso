local embedding_dim = std.parseJson(std.extVar('embedding_dim'));
local hidden_size = std.parseJson(std.extVar('hidden_size'));

{
  "dataset_reader": {
    "type": "seq2seq",
    "source_add_start_token": false,
    "source_add_end_token": false,
    "target_add_start_token": true,
    "target_add_end_token": true,
    "start_symbol": "@",
    "end_symbol": " ",
    "source_tokenizer": {
      "type": "character"
    },
    "target_tokenizer": {
      "type": "character"
    },
    "source_token_indexers": {
      "tokens": {
        "type": "single_id",
        "namespace": "source_tokens"
      }
    },
    "target_token_indexers": {
      "tokens": {
        "namespace": "target_tokens"
      }
    }
  },
  "train_data_path": "data/training_500000.csv",
  "validation_data_path": "data/validation_10000.csv",
  "model": {
    "type": "composed_seq2seq",
    "source_text_embedder": {
      "token_embedders": {
        "tokens": {
          "type": "embedding",
          "vocab_namespace": "source_tokens",
          "embedding_dim": embedding_dim,
          "trainable": true
        }
      }
    },
    "encoder": {
      "type": "lstm",
      "input_size": embedding_dim,
      "hidden_size": hidden_size,
      "num_layers": 1
    },
    "decoder": {
      "decoder_net": {
        "type": "lstm_cell",
        "decoding_dim": hidden_size,
        "target_embedding_dim": embedding_dim,
        "attention": {
          "type": "dot_product"
        }
      },
      "max_decoding_steps": 11, // "1234-67-90 "
      "target_namespace": "target_tokens",
      "target_embedder": {
        "vocab_namespace": "target_tokens",
        "embedding_dim": embedding_dim
      },
      "scheduled_sampling_ratio": 0.5,
      "beam_size": 10,
      "token_based_metric": "my_metrics"
    }
  },
  "data_loader": {
    "batch_size": 32
  },
  "trainer": {
    "num_epochs": 30,
    "patience": 5,
    "validation_metric": "+sequence_accuracy",
    "optimizer": {
      "type": "adam",
      "lr": 0.01
    },
    "num_serialized_models_to_keep": 2,
    "callbacks": [
      {
        "type": "wandb_allennlp",
        "files_to_save": ["config.json"],
        "files_to_save_at_end": ["*.tar.gz"]
      },
      {
        "type": "console_logger",
        "should_log_inputs": false
      }
    ],
    "cuda_device": -1
  }
}
