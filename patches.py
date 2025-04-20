from app import app, oidc
from models import db,Catalog, Patches
from flask import render_template, request, redirect
from utils import get_user_info

@app.route('/patches')
@oidc.require_login
def admin_patches():
    # Get user info
    user_info = get_user_info()
    
    catalog = Catalog.query.all()
    
    patches_data = []
    patches = Patches.query.all()
    
    for patch in patches:
        item = Catalog.query.filter_by(item_id=patch.item_id).first()
        item_name = item.name if item else "Unknown"
        
        patches_data.append({
            "patch_id": patch.patch_id,
            "item_id": patch.item_id,
            "item_name": item_name,
            "content_id": patch.content_id
        })
    
    return render_template('index.html', catalog=catalog, patches=patches_data, user_info=user_info, main=True)

@app.route('/patches/new', methods=['GET', 'POST'])
@oidc.require_login
def new_patch():
    catalog = Catalog.query.all()

    user_info = get_user_info()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        content_id = request.form.get('content_id')
        
        # Create new patch
        new_patch = Patches(item_id=item_id, content_id=content_id)
        db.session.add(new_patch)
        db.session.commit()
        
        return redirect('/patches')
    
    return render_template('patch_form.html', catalog=catalog, user_info=user_info)

@app.route('/patches/edit/<int:patch_id>', methods=['GET', 'POST'])
@oidc.require_login
def edit_patches(patch_id):
    patches_item = Patches.query.get_or_404(patch_id)
    catalog = Catalog.query.all()
    
    user_info = get_user_info()

    if request.method == 'POST':
        patches_item.patch_id = request.form.get('patch_id')
        patches_item.item_id = request.form.get('item_id')
        patches_item.content_id = request.form.get('content_id')
        
        db.session.commit()
        
        return redirect('/patches')

    return render_template('patch_edit.html',
                           item=patches_item,
                           user_info=user_info,
                           catalog=catalog)

@app.route('/patches/delete/<int:patch_id>', methods=['GET', 'POST'])
@oidc.require_login
def delete_patch(patch_id):
    patch = Patches.query.get_or_404(patch_id)
    
    if request.method == 'POST':
        try:
            db.session.delete(patch)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error deleting patch: {e}")
        
        return redirect('/patches')
    
    user_info = get_user_info()
    
    catalog_item = Catalog.query.filter_by(item_id=patch.item_id).first()
    
    return render_template('patch_delete.html',
                          patch=patch,
                          catalog_item=catalog_item,
                          user_info=user_info)