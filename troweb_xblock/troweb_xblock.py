from urllib.parse import urlparse

import pkg_resources
import requests
from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Integer, Scope, String
from jinja2 import Template

class TrowebXBlock(XBlock):
    """
    An XBlock providing oEmbed capabilities for video
    """

    href = String(
        help="URL of the video page at the provider", default=None, scope=Scope.content
    )
    maxwidth = Integer(
        help="Maximum width of the video", default=800, scope=Scope.content
    )
    maxheight = Integer(
        help="Maximum height of the video", default=450, scope=Scope.content
    )

    def resource_string(self, path):
        """Handy helper for getting resources from our kit."""
        data = pkg_resources.resource_string(__name__, path)
        return data.decode("utf8")

    def resource_filename(self, path):
        """Handy helper for getting resources names from our kit."""
        name = pkg_resources.resource_filename(__name__ , path)
        return name

    def student_view(self, context=None):
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused).

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """
        provider, embed_code = self.get_embed_code_for_url(self.href)
        # Load the HTML fragment from within the package and fill in the template
        html = self.resource_string("static/html/troweb.html")
        frag = Fragment(html.format(self=self, embed_code=embed_code))

        # Load CSS
        frag.add_css(self.resource_string("static/css/troweb.css"))

        # Load JS
        if provider == 'vimeo.com':
            # Load the Froogaloop library from vimeo CDN.
            frag.add_javascript_url(
                "//cdn.jsdelivr.net/npm/vimeo-froogaloop2@0.1.1/javascript/froogaloop.js"
                )
            frag.add_javascript(self.resource_string("static/js/src/troweb.js"))
            frag.initialize_js("TrowebXBlock")

        return frag

    def get_embed_code_for_url(self, url):
        """
        Get the code to embed from the oEmbed provider.
        """
        hostname = url and urlparse(url).hostname
        # Check that the provider is supported
        if hostname == "vimeo.com":
            oembed_url = "http://vimeo.com/api/oembed.json"
        else:
            return hostname, "<p>Unsupported video provider ({0})</p>".format(hostname)

        params = {
            "url": url,
            "format": "json",
            "maxwidth": self.maxwidth,
            "maxheight": self.maxheight,
            "api": True,
        }

        try:
            r = requests.get(oembed_url, params=params, timeout=10)
            r.raise_for_status()
        except Exception as e:
            return (
                hostname,
                "<p>Error getting video from provider ({error})</p>".format(error=e),
            )
        response = r.json()

        return hostname, response["html"]

    @XBlock.json_handler
    def studio_submit(self, data, suffix=''):
        """
        Called when submitting the form in Studio.
        """
        self.href = data.get('href')
        self.maxwidth = data.get('maxwidth')
        self.maxheight = data.get('maxheight')

        return {'result': 'success'}

    def render_troweb_edit_html(self):
        # res = requests.get('ac-endpoint' , headers = {})
        # res = res.json()
        res = [
            {
                "file_id":"111",
                "pk":1,
                "name":"salam.mp4",
                "size":10,
                "blob_type":"video",
                "type":"app/pdf",
                "uploaded":"2022"
            },
            {
                "file_id":"222",
                "pk":2,
                "name":"by.jpg",
                "size":20,
                "blob_type":"image",
                "type":"image/png",
                "uploaded":"2023"
            },
        ]
        dest_html_name = 'static/html/troweb_edit.html'
        html_template = self.resource_string('templates/html/troweb_edit.template.html')
        dest_html_abs_path = self.resource_filename(dest_html_name)
        template = Template(html_template)
        with open(dest_html_abs_path , 'w') as file:
            file.write(template.render(res = res))
        return self.resource_string(dest_html_name)

    def studio_view(self, context):
        """
        Create a fragment used to display the edit view in the Studio.
        """
        rendered_html = self.render_troweb_edit_html()
        frag = Fragment(rendered_html)
        frag.add_css(self.resource_string("static/css/troweb.css"))
        frag.add_javascript(self.resource_string("static/js/src/troweb_edit.js"))
        frag.initialize_js("TrowebEditBlock")
        return frag

    # workbench while developing your XBlock.
    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            (
                "TrowebXBlock",
                """<troweb_xblock href="https://vimeo.com/253989945" maxwidth="800"/>""",
            ),
            (
                "Multiple TrowebXBlock",
                """
                <vertical_demo>
                <troweb_xblock href="https://vimeo.com/253989945" maxwidth="800"/>
                <troweb_xblock href="https://vimeo.com/253989945" maxwidth="800"/>
                <troweb_xblock href="https://vimeo.com/253989945" maxwidth="800"/>
                </vertical_demo>
                """,
            ),
        ]
