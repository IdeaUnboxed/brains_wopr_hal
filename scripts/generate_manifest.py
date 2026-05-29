import os
import json
from datetime import datetime

def generate_manifest():
    base_dir = '.'
    manifest = {
        'last_updated': datetime.utcnow().isoformat(),
        'logs': [],
        'fragments': []
    }
    
    # Scan logs
    log_dir = os.path.join(base_dir, 'logs')
    if os.path.exists(log_dir):
        for f in sorted(os.listdir(log_dir), reverse=True):
            if f.endswith('.log'):
                manifest['logs'].append(f)
                
    # Scan fragments
    frag_dir = os.path.join(base_dir, 'archival_fragments')
    if os.path.exists(frag_dir):
        for f in sorted(os.listdir(frag_dir)):
            manifest['fragments'].append(f)
            
    with open('manifest.json', 'w') as f:
        json.dump(manifest, f, indent=2)
    print('Manifest generated successfully.')

if __name__ == '__main__':
    generate_manifest()
