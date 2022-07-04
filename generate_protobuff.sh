#!/bin/bash

# Usefull article at: https://blog.lelonek.me/a-brief-introduction-to-grpc-in-go-e66e596fe244
echo "Generating subs from proto buffers. Entering protobuffers directory..."
cd protobuffers
protoc --go-grpc_out=. *.proto
if [ $? -ne 0 ]; then
  echo "Unable to generate Go stubs. Exiting..."
  exit 1
fi

echo "Go Stubs generated. Now I am going to move them to option directory..."
mv *.go ../option/

if [ $? -ne 0 ]; then
  echo "Unable to move Go stubs. Exiting..."
  exit 1
fi

python -m grpc_tools.protoc --proto_path=. *.proto --python_out=. --grpc_python_out=.
if [ $? -ne 0 ]; then
  echo "Unable to generate Python stubs. Exiting..."
  exit 1
fi

echo "Python Stubs generated. Now I am going to move them to option directory..."
mv *.py ../option/

if [ $? -ne 0 ]; then
  echo "Unable to move Python stubs. Exiting..."
  exit 1
fi

echo "Done."
