#!/usr/bin/env python3

from metatools.version import generic

def create_transform(transform_data):
	def transform_lambda(tag):
		for trans_dict in transform_data:
			if "kind" not in trans_dict:
				raise ValueError("Please specify 'kind' for gitlab transform: element.")
			kind = trans_dict['kind']
			if kind == "string":
				match = trans_dict['match']
				replace = trans_dict['replace']
				tag = tag.replace(match, replace)
			else:
				raise ValueError(f"Unknown 'kind' for github transform: {kind}")
		return tag
	return transform_lambda

async def generate(hub, **pkginfo):
	user = pkginfo["name"]
	repo = pkginfo["name"]
	server = "https://gitlab.com"

	if "gitlab_user" in pkginfo:
		user = pkginfo["gitlab_user"]
	elif "gitlab" in pkginfo and "user" in pkginfo["gitlab"]:
		user = pkginfo["gitlab"]["user"]

	if "gitlab_repo" in pkginfo:
		repo = pkginfo["gitlab_repo"]
	elif "gitlab" in pkginfo and "repo" in pkginfo["gitlab"]:
		repo = pkginfo["gitlab"]["repo"]

	if "gitlab_server" in pkginfo:
		server = pkginfo["gitlab_server"]
	elif "gitlab" in pkginfo and "server" in pkginfo["gitlab"]:
		server = pkginfo["gitlab"]["server"]

	query = pkginfo["gitlab"]["query"]
	if query not in ["releases", "tags", "snapshot"]:
		raise KeyError(
			f"{pkginfo['cat']}/{pkginfo['name']} should specify GitLab query type of 'releases', 'tags' or 'snapshot'."
		)
	if query == "tags":
		project_path = f"{user}%2F{repo}"
		info_url = f"https://{server}/api/v4/projects/{project_path}/repository/tags"
	elif query == "releases":
		if "project_id" not in pkginfo["gitlab"]:
			raise KeyError("To query releases, we require a project ID defined in gitlab/project_id")
		project_id = pkginfo["gitlab"]["project_id"]
		info_url = f"https://{server}/api/v4/projects/{project_id}/releases"


	tags_dict = await hub.pkgtools.fetch.get_page(
		info_url, is_json=True
	)

	versions = [generic.parse(tag["name"]) for tag in tags_dict if not tag["name"].lstrip("v").upper().isupper() ]
	version = max(versions).public
	artifact = hub.pkgtools.ebuild.Artifact(
		url=f"https://gitlab.freedesktop.org/{user}/{repo}/-/archive/{version}/{repo}-v{version}.tar.bz2"
	)

	ebuild = hub.pkgtools.ebuild.BreezyBuild(
		**pkginfo,
		version=version,
		artifacts=[artifact],
	)
	ebuild.push()

# vim: ts=4 sw=4 noet
