"""
Test: What does Flask pass to dashboard template?
"""
from app import create_app
from unittest.mock import patch
import json

app = create_app()

# Patch render_template to capture arguments
original_render_template = None
captured_context = {}

def mock_render_template(template_name, **kwargs):
    """Capture template context"""
    captured_context.update(kwargs)
    print(f"\n📄 Captured template context for: {template_name}")
    return f"Mock HTML for {template_name}"

with app.app_context():
    with app.test_client() as client:
        print("=" * 60)
        print("TESTING: What Flask passes to dashboard template?")
        print("=" * 60)
        
        # Login
        print("\n1️⃣  Logging in...")
        client.post('/auth/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        
        # Patch render_template before calling dashboard
        print("\n2️⃣  Calling dashboard route with patched render_template...")
        
        from flask import render_template as original_rt
        import app.routes.dashboard as dashboard_module
        
        # Store original
        original_render = dashboard_module.render_template
        
        # Replace with mock
        def capture_render(template, **kwargs):
            captured_context.update(kwargs)
            return "mock"
        
        dashboard_module.render_template = capture_render
        
        try:
            resp = client.get('/dashboard')
            print(f"\n✓ Dashboard response status: {resp.status_code}")
        finally:
            dashboard_module.render_template = original_render
        
        # Show captured context
        print("\n" + "=" * 60)
        print("📊 TEMPLATE CONTEXT (from Flask)")
        print("=" * 60)
        
        if captured_context:
            for key, value in captured_context.items():
                if key == 'data_terbaru':
                    print(f"\n{key}:")
                    if value:
                        for item in value[:2]:
                            print(f"  - {item.no_spk}")
                        if len(value) > 2:
                            print(f"  ... and {len(value) - 2} more")
                    else:
                        print("  (empty)")
                elif key in ['per_kategori', 'per_jenis_trouble', 'per_perangkat']:
                    print(f"\n{key}: {json.dumps(value, indent=2)}")
                elif key == 'trend_bulanan':
                    print(f"\n{key}: {len(value)} months")
                    print(f"  First: {value[0]}")
                    print(f"  Last: {value[-1]}")
                else:
                    print(f"\n{key}: {value}")
        else:
            print("❌ No context captured!")
