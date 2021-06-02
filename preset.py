import typing, pathlib
from xml.etree import ElementTree

def make_preset(server:str, port:int=4000, settings:typing.Union[dict[str,str],None]=None) -> str:
	"""Output XML for a NoMachine Connection Preset to a given server"""
	
	connection_settings = {
		"Connection service": "nx",
		"NoMachine daemon port": str(port),
		"Server host": server
	}

	addtl_settings = {
		"Show remote audio alert message": "false",
		"Show remote display resize message": "false",
		"Show remote desktop view mode message": "false"
	}

	if isinstance(settings, dict):
		addtl_settings.update(settings)

	root = ElementTree.Element("NXClientSettings", {"version":"2.0", "application":"nxclient"})
	grp_general = ElementTree.SubElement(root, "group", {"name":"General"})

	# Connection properties
	for key, value in connection_settings.items():
		grp_general.append(ElementTree.Element("option", {"key":key, "value": value}))
	
	# Additional settings
	for key, value in addtl_settings.items():
		grp_general.append(ElementTree.Element("option", {"key":key, "value": value}))
	
	# Embed thumbnail
	grp_general.append(ElementTree.Element("option",{"key":"Session screenshot", "value":make_thumbnail()}))
	
	# Generate XML as utf-8 string
	docstring = "<!DOCTYPE NXClientSettings>"
	return docstring + ElementTree.tostring(root, encoding="utf-8").decode("utf-8")

def make_thumbnail(path:typing.Union[pathlib.Path, str, None]=None) -> str:
	"""Encode thumbnail as base64"""
	with open("res/nm_thumb_default.b64") as b64:
		return b64.read()


if __name__ == "__main__":

	import sys
	
	if len(sys.argv) < 2:
		print(f"Usage: {sys.argv[0]} server_address [output_file_path.nxs]", file=sys.stderr)
		sys.exit(1)
	
	# Build filename either from the one provided, or from the servername
	filename = pathlib.Path(sys.argv[2] if len(sys.argv)<2 else sys.argv[1]+".nxs").with_suffix(".nxs")

	try:
		filename.write_text(make_preset(sys.argv[1]))
	except Exception as e:
		print(f"Error writing NXS file to {filename}: {e}", file=sys.stderr)
		sys.exit(1)
	else:
		print(f"Successfully wrote preset for {sys.argv[1]} to {filename}")
		sys.exit(0)