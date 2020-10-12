#!/bin/bash

# Usefull article at: https://blog.lelonek.me/a-brief-introduction-to-grpc-in-go-e66e596fe244
echo "Generating subs from proto buffers. Entering protobuffers directory..."
cd protobuffers
protoc --go_out=plugins=grpc:. *.proto

if [ $? -ne 0 ]; then
  echo "Unable to generate stubs. Exiting..."
  exit 1
fi

echo "Stubs generated. Now I am going to move them to option directory..."
mv *.go ../option/

if [ $? -ne 0 ]; then
  echo "Unable to generate stubs. Exiting..."
  exit 1
fi

echo "Done."
