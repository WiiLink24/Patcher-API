from app import app
from models import Catalog, Patches
from flask import jsonify


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
