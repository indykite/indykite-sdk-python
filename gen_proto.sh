
echo "Generating protobufs..."
buf generate buf.build/indykite/indykiteapis
buf generate buf.build/envoyproxy/protoc-gen-validate
buf generate buf.build/bufbuild/protovalidate
buf generate buf.build/gnostic/gnostic

echo "Rewriting imports..."
packages=("indykite" "validate" "buf" "gnostic")

if [[ $OSTYPE == 'darwin'* ]]; then
        for package in ${packages[@]}; do
                find indykite_sdk/indykite/. -name '*.py' -exec sed -i '' -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
        done
else
        for package in ${packages[@]}; do
                find indykite_sdk/indykite/. -name '*.py' -exec sed -i -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
                find indykite_sdk/buf/validate/. -name '*.py' -exec sed -i -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
                find indykite_sdk/gnostic/. -name '*.py' -exec sed -i -e "s/from ${package}/from indykite_sdk.${package}/g" {} \;
        done
fi

echo "Done"
