import json

def verify_files():
    # Check the before file
    with open('complete_all_categories_before.json', 'r', encoding='utf-8') as f:
        before_data = json.load(f)
    
    # Check the after file
    with open('complete_all_categories_after.json', 'r', encoding='utf-8') as f:
        after_data = json.load(f)
    
    print(f"Categories in before file: {len(before_data)}")
    print(f"Categories in after file: {len(after_data)}")
    
    total_before = sum(len(cat) for cat in before_data)
    total_after = sum(len(cat) for cat in after_data)
    
    print(f"Total prompts in before file: {total_before}")
    print(f"Total prompts in after file: {total_after}")
    
    # Show categories
    print("\nCategories:")
    for i, cat in enumerate(before_data):
        if cat:
            print(f"  {i+1}. {cat[0]['category']} - {len(cat)} prompts")
    
    # Check vulnerable counts
    vulnerable_before = 0
    vulnerable_after = 0
    
    for cat in before_data:
        for item in cat:
            if item.get('vulnerable', False):
                vulnerable_before += 1
    
    for cat in after_data:
        for item in cat:
            if item.get('vulnerable', False):
                vulnerable_after += 1
    
    print(f"\nVulnerable responses:")
    print(f"  Before hardening: {vulnerable_before}")
    print(f"  After hardening: {vulnerable_after}")
    print(f"  Improvement: {vulnerable_before - vulnerable_after} responses hardened")

if __name__ == "__main__":
    verify_files()