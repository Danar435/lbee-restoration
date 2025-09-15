#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path>"
  exit 1
fi

input_path="$1"
output_path="./output"
lucksystem_bin="./lucksystem"

if [ ! -f "$lucksystem_bin" ]; then
  echo "Error: $lucksystem_bin not found!"
  exit 1
fi

if [ ! -d "$input_path" ]; then
  echo "Error: $input_path is not a directory!"
  exit 1
fi

if [ ! -f "$input_path/LITBUS_WIN32.exe" ]; then
  echo "Error: $input_path/LITBUS_WIN32.exe not found!"
  echo 
  echo "Double-check that the path leads to the game's root directory."
  echo "Example: ~/.local/share/Steam/steamapps/common/Little Busters!\ English\ Edition"
  exit 1
fi

mkdir -p "$output_path"
mkdir -p "$output_path/files"
cp "./source/system.cnf" "$output_path/"

repack() {
    file="$1"
    pak=${file^^}.PAK

    if [ ! -f "$input_path/files/$pak" ]; then
        echo "Error: $input_path/files/$pak not found!"
        exit 1
    fi

    echo "Processing $pak..."

    mkdir -p "$output_path/$file-temp"
    $lucksystem_bin "pak" "extract" -s "$input_path/files/$pak" -i "$input_path/files/$pak" -o "$output_path/temp" -a "$output_path/$file-temp"
    rm "$output_path/temp"
    cp -r "./source/$file-done/" "$output_path/$file-temp/"
    $lucksystem_bin "pak" "replace" -s "$input_path/files/$pak" -i "$output_path/$file-temp" -o "$output_path/files/$pak"
    rm -r "$output_path/$file-temp"
}

repack "battle"
repack "bgcg"
repack "charcg"
repack "eventcg"
repack "gencg"
repack "othcg"
repack "parts"
repack "pt"
repack "syscg"

echo "Repacking completed! Check the '$output_path' directory for results."
exit 0
