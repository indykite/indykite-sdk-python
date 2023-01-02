
echo "Generating protobufs..."
buf generate buf.build/indykite/indykiteapis
buf generate buf.build/envoyproxy/protoc-gen-validate

echo "Rewriting imports..."
packages=("indykite" "validate")

if [[ $OSTYPE == 'darwin'* ]]; then
        for package in ${packages[@]}; do
                find indykite_sdk/indykite/. -name '*.py' -exec sed -i '' -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
        done
else
        for package in ${packages[@]}; do
                find indykite_sdk/indykite/. -name '*.py' -exec sed -i -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
        done
fi

echo "Done"
