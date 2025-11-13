#!/usr/bin/env python3
# Quick test of Bengali language detection

test_texts = [
    "আমার ধানের পাতা হলুদ হয়ে যাচ্ছে",
    "My rice leaves are turning yellow",
    "ধান",
    "আমি",
]

for text in test_texts:
    bengali_count = 0
    for char in text:
        if '\u0980' <= char <= '\u09FF':
            bengali_count += 1
    
    print(f"Text: {text}")
    print(f"  Repr: {repr(text)}")
    print(f"  Bengali chars: {bengali_count}")
    print(f"  Length: {len(text)}")
    print()
