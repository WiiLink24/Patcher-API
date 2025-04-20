from app import app, oidc
from models import db,Catalog, Patches
from flask import jsonify, render_template, request, redirect
from utils import get_user_info

@app.route("/api/catalog/all")
def all_catalog():
    titles = Catalog.query.all()

    ret = []

    for title in titles:
        patches = Patches.query.filter_by(item_id=title.item_id).all()

        patch_list = []
        for patch in patches:
            patch_list.append(patch.content_id)

        ret.append({
            "item_id": title.item_id,
            "name": title.name,
            "title_id": title.title_id,
            "latest_version": title.latest_version,
            "patches": patch_list
        })

    return jsonify(ret)

@app.route('/catalog/new', methods=['GET', 'POST'])
@oidc.require_login
def new_catalog():
    user_info = get_user_info()

    if request.method == 'POST':
        item_id = request.form.get('item_id')
        name = request.form.get('name')
        title_id = request.form.get('title_id')
        latest_version = request.form.get('latest_version')
        
        # Create new patch
        new_catalog = Catalog(item_id=item_id,name=name, title_id=title_id, latest_version=latest_version)
        db.session.add(new_catalog)
        db.session.commit()
        
        return redirect('/patches')

    return render_template('catalog_form.html', user_info=user_info)

@app.route('/catalog/edit/<int:item_id>', methods=['GET', 'POST'])
@oidc.require_login
def edit_catalog(item_id):
    catalog_item = Catalog.query.get_or_404(item_id)
    patches = Patches.query.filter_by(item_id=item_id).all()
    
    user_info = get_user_info()

    if request.method == 'POST':
        catalog_item.name = request.form.get('name')
        catalog_item.title_id = request.form.get('title_id')
        catalog_item.latest_version = request.form.get('latest_version')
        
        db.session.commit()
        
        return redirect('/patches')

    return render_template('catalog_edit.html',
                           item=catalog_item,
                           user_info=user_info,
                           patches=patches)