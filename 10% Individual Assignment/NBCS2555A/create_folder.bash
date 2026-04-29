#!/bin/bash

if [ ! -f "list.txt" ]; then
  echo "Error: File list.txt tidak ditemukan."
  exit 1
fi

while IFS= read -r line; do
  cleaned_name=$(echo "$line" | sed 's/[[:space:]]*$//')

  cleaned_name=$(echo "$cleaned_name" | sed 's/[^a-zA-Z0-9._-]*$//')

  if [ -n "$cleaned_name" ]; then
    if [ ! -d "$cleaned_name" ]; then
      mkdir "$cleaned_name"
      echo "Folder '$cleaned_name' telah dibuat."

      echo "# $cleaned_name" > "$cleaned_name/README.md"
      echo "File README.md telah dibuat di dalam '$cleaned_name'."
    else
      echo "Folder '$cleaned_name' sudah wujud."
    fi
  fi
done < "list.txt"

echo "Selesai membuat folder dan file README.md."

exit 0
