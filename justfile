set shell := ["powershell", "-NoProfile", "-Command"]

OPENAPI := "openapi.yaml"

OUTDIR := "generated"

GENERATOR := "python"

generate-models:
    openapi-generator-cli generate \
        -i {{OPENAPI}} \
        -g {{GENERATOR}} \
        -o {{OUTDIR}} \
        --global-property models,modelTests=false,modelDocs=false \
        --skip-validate-spec