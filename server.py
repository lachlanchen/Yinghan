import json
import os
import time
import uuid

import tornado.ioloop
import tornado.web

from organoid_segmenter import segment_organoid


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class SegmentHandler(tornado.web.RequestHandler):
    async def post(self):
        if "image" not in self.request.files:
            self.set_status(400)
            self.finish({"error": "Missing file field 'image'"})
            return

        image_file = self.request.files["image"][0]
        filename = image_file.get("filename", "upload.jpg")
        ext = os.path.splitext(filename)[1] or ".jpg"

        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        upload_name = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex}{ext}"
        upload_path = os.path.join(UPLOAD_DIR, upload_name)

        with open(upload_path, "wb") as f:
            f.write(image_file["body"])

        model = self.get_argument("model", "gpt-4o-2024-08-06")

        try:
            result = segment_organoid(upload_path, out_dir=OUTPUT_DIR, model=model)
        except Exception as exc:
            self.set_status(500)
            self.finish({"error": str(exc), "error_type": type(exc).__name__})
            return

        response = {
            "width": result.width,
            "height": result.height,
            "polygon": result.polygon,
            "confidence": result.confidence,
            "annotated_url": f"/outputs/{os.path.basename(result.annotated_path)}",
            "mask_url": f"/outputs/{os.path.basename(result.mask_path)}",
            "json_url": f"/outputs/{os.path.basename(result.json_path)}",
            "upload_url": f"/uploads/{os.path.basename(upload_path)}",
        }

        self.set_header("Content-Type", "application/json")
        self.finish(json.dumps(response))


def make_app() -> tornado.web.Application:
    return tornado.web.Application(
        [
            (r"/", IndexHandler),
            (r"/api/segment", SegmentHandler),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": STATIC_DIR}),
            (r"/uploads/(.*)", tornado.web.StaticFileHandler, {"path": UPLOAD_DIR}),
            (r"/outputs/(.*)", tornado.web.StaticFileHandler, {"path": OUTPUT_DIR}),
        ],
        template_path=TEMPLATE_DIR,
        static_path=STATIC_DIR,
        autoreload=True,
    )


if __name__ == "__main__":
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    app = make_app()
    app.listen(8888)
    print("Server running at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
