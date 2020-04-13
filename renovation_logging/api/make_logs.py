import frappe
from six import string_types


@frappe.whitelist(allow_guest=True)
def log_info(content, title=None, tags=None, user=None):
  return make_log(
      log_type="Info", content=content, title=title, tags=tags, user=user
  )


@frappe.whitelist(allow_guest=True)
def log_warning(content, title=None, tags=None, user=None):
  return make_log(
      log_type="Warning", content=content, title=title, tags=tags, user=user
  )


@frappe.whitelist(allow_guest=True)
def log_error(content, title=None, tags=None, user=None):
  return make_log(
      log_type="Error", content=content, title=title, tags=tags, user=user
  )


@frappe.whitelist(allow_guest=True)
def log_request(
    request=None, response=None, http_code=None, meta=None, user=None
):
  return make_log(
      log_type="Request",
      request=request,
      response=response,
      http_code=http_code,
      req_meta=meta,
      user=user
  )


@frappe.whitelist(allow_guest=True)
def make_log(
    log_type,
    content=None,
    title=None,
    tags=None,
    request=None,
    http_code=None,
    response=None,
    req_meta=None,
    user=None
):
  doc = frappe._dict(doctype="Renovation Log")

  if tags:
    doc.tags = []
    for t in sync_tags(tags):
      doc.tags.append(frappe._dict(tag=t))

  if user:
    doc.user = user

  doc.type = log_type
  if log_type in ("Info", "Warning", "Error"):
    doc.content = content
    doc.title = title
  elif log_type in ("Request"):
    doc.request = "{}{}".format(
        request, "\n\n{}".format(req_meta) if req_meta else ""
    )
    doc.http_code = http_code
    doc.response = response
  else:
    frappe.throw("Invalid type: {}".format(log_type))

  return frappe.get_doc(doc).insert(ignore_permissions=True)


def sync_tags(tags):
  if isinstance(tags, string_types):
    if tags.startswith("["):
      tags = frappe.parse_json(tags)
    else:
      tags = [tags]

  for t in tags:
    if not frappe.db.exists("Renovation Log Tag", t):
      frappe.get_doc(frappe._dict(doctype="Renovation Log Tag",
                                  tag=t)).insert(ignore_permissions=True)

  return set(tags)
