DSFLAGS=(--env-file <HOME>/.config/devx-bench/deepseek.env --model deepseek-flash
 --codex-config 'model_provider="deepseek"' --codex-config 'model_providers.deepseek.name="DeepSeek"'
 --codex-config 'model_providers.deepseek.base_url="https://api.deepseek.com"'
 --codex-config 'model_providers.deepseek.env_key="DEEPSEEK_API_KEY"'
 --codex-config 'model_providers.deepseek.wire_api="responses"')
