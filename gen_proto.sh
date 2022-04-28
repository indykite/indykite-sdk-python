
echo "Generating protobufs ..."
buf generate buf.build/indykite/indykiteapis
buf generate buf.build/envoyproxy/protoc-gen-validate 

echo "Rewriting the imports..."
packages=("indykite" "validate")

for package in ${packages[@]}; do
        find jarvis_sdk/indykite/. -name '*.py' -exec sed -i '' -e "s/from ${package}/from jarvis_sdk.${package}/g" {} \;
done

echo "Done"