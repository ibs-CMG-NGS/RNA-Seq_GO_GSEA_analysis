import yaml
import json

with open("workflow/config/batch_gsea_config.yaml") as f:
    cfg = yaml.safe_load(f)

print("Mode in base_config:", cfg["base_config"]["gsea"]["mode"])
print("\nFull gsea config:")
print(json.dumps(cfg["base_config"]["gsea"], indent=2))
