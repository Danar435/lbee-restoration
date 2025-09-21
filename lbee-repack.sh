#!/bin/bash

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/game/folder/"
  exit 1
fi

input_path=$1
output_path=./output
lucksystem_bin=./lucksystem
lb_repack_path=./LB_repack

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
  echo "Double-check and make sure that the path leads to the game's root directory."
  exit 1
fi

echo "Processing auxillary files..."

mkdir -p "$output_path/files/movie/low"
cp ./source/auxiliary-files/system.cnf "$output_path/"
cp ./source/auxiliary-files/movie/AYA.webm "$output_path/files/movie/AYA.webm"
cp ./source/auxiliary-files/movie/EDAL_en.webm "$output_path/files/movie/EDAL_en.webm"
cp ./source/auxiliary-files/movie/EDAL.webm "$output_path/files/movie/EDAL.webm"
cp ./source/auxiliary-files/movie/OP00_en.webm "$output_path/files/movie/OP00_en.webm"
cp ./source/auxiliary-files/movie/OP00.webm "$output_path/files/movie/OP00.webm"
cp ./source/auxiliary-files/movie/EDAL_en.webm "$output_path/files/movie/low/EDAL_en.webm"
cp ./source/auxiliary-files/movie/EDAL.webm "$output_path/files/movie/low/EDAL.webm"
cp ./source/auxiliary-files/movie/OP00_og.webm "$output_path/files/movie/low/OP00_en.webm"
cp ./source/auxiliary-files/movie/OP00_og.webm "$output_path/files/movie/low/OP00.webm"

repack() {
  file="$1"
  pak=$(echo "$file" | tr '[:lower:]' '[:upper:]').PAK

  if [ ! -f "$input_path/files/$pak" ]; then
      echo "Error: $input_path/files/$pak not found!"
      exit 1
  fi

  echo "Processing $pak..."

  mkdir -p "$output_path/$file-temp"
  "$lucksystem_bin" pak extract -s "$input_path/files/$pak" -i "$input_path/files/$pak" -o "$output_path/temp" -a "$output_path/$file-temp" > /dev/null 2>&1
  rm "$output_path/temp"
  cp -r ./source/$file-done/* "$output_path/$file-temp/"
  "$lucksystem_bin" pak replace -s "$input_path/files/$pak" -i "$output_path/$file-temp" -o "$output_path/files/$pak" > /dev/null 2>&1
  rm -r "$output_path/$file-temp"
}

rewrite() {
  file=$1
  pak=$(echo "$file" | tr '[:lower:]' '[:upper:]').PAK

  if [ ! -d "$lb_repack_path" ]; then
      echo "Warning: $lb_repack_path not found! Skipping $pak"
      return
  fi

  if ! command -v python3 &> /dev/null; then
      echo "Warning: python3 not installed! Skipping $pak"
      return
  fi

  if [ ! -f $input_path/files/$pak ]; then
      echo "Error: $input_path/files/$pak not found!"
      exit 1
  fi

  echo "Processing $pak..."

  cd $lb_repack_path
  mkdir -p ./core
  mkdir -p ./SCRIPT
  mv ./steam/*.py ./ > /dev/null 2>&1
  mv ./steam/core/opcode_steam.txt ./core/opcode_steam.txt > /dev/null 2>&1
  cp $input_path/files/$pak ./SCRIPT/SCRIPT_steam.PAK

  python3 unpack.py > /dev/null 2>&1
  cp -r ../source/script-done/* ./SCRIPT/disassembled/
  python3 repack.py > /dev/null 2>&1
  mv ./SCRIPT/SCRIPT_repacked.PAK ../$output_path/files/$pak
  cd ../
}

repack "battle"
repack "bgcg"
repack "charcg"
repack "eventcg"
repack "gencg"
repack "gm"
repack "othcg"
repack "parts"
repack "pt"
repack "syscg"
rewrite "script"

echo "Patching completed! Check the '$output_path' directory for the patched files."
exit 0
