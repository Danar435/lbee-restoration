#!/bin/bash

output_path="./output"
lucksystem_bin="./lucksystem"
use_censored=false

show_help() {
  echo "Usage: $0 [options] /path/to/game/folder/"
  echo
  echo "Options:"
  echo "  -c, --censor          Patch using censored assets     (default: false)"
  echo "  -o, --output DIR      Specify output directory        (default: ./output)"
  echo "  -l, --lucksystem PATH Specify LuckSystem binary path  (default: ./lucksystem)"
  echo "  -h, --help            Show this help message"
  echo
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -o|--output)
      output_path="$2"
      shift 2
      ;;
    -l|--lucksystem)
      lucksystem_bin="$2"
      shift 2
      ;;
    -c|--censor)
      use_censored=true
      shift
      ;;
    -h|--help)
      show_help
      ;;
    -*|--*)
      echo "Unknown option $1"
      show_help
      ;;
    *)
      if [ -z "$input_path" ]; then
        input_path="$1"
      else
        echo "Error: Multiple input paths specified"
      fi
      shift
      ;;
  esac
done

if [ -z "$input_path" ]; then
  show_help
fi

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
  echo "Make sure that the path leads to the game's root directory."
  exit 1
fi

echo "Processing auxillary files..."

mkdir -p "$output_path/files"
cp ./source/auxiliary-files/system.cnf "$output_path/"
cp -r ./source/auxiliary-files/movie "$output_path/files/"

if [ "$use_censored" = true ]; then
  echo "Processing censored assets..."

  rm -r ./source/eventcg-done/
  cp -r ./source/auxiliary-files/clean/eventcg-done ./source/eventcg-done
  cp ./source/auxiliary-files/clean/SEEN0520 ./source/script-done/SEEN0520
  cp ./source/auxiliary-files/clean/NYKD_MASK01 ./source/othcg-done/NYKD_MASK01
fi


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
  cp -r "./source/$file-done/"* "$output_path/$file-temp/"
  "$lucksystem_bin" pak replace -s "$input_path/files/$pak" -i "$output_path/$file-temp" -o "$output_path/files/$pak" > /dev/null 2>&1
  rm -r "$output_path/$file-temp"
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
repack "script"

echo "Patching completed!"
echo "Check the '$output_path' directory for the patched files."
exit 0
