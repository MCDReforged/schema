import argparse
import json
from pathlib import Path
from typing import Type, cast

from pydantic import BaseModel

from mcdreforged.mcdr_config import MCDReforgedConfig
from mcdreforged.permission.permission_manager import PermissionConfigModel
from mcdreforged.plugin.meta.schema import PluginMetadataJsonModel
from mcdreforged.plugin.type.directory_plugin import LinkedDirectoryPluginJsonModel


def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-o', '--output-dir', default='schemas')
	args = parser.parse_args()

	output_dir = Path(args.output_dir)

	def generate(clazz: Type[BaseModel]):
		url = cast(str, cast(dict, clazz.model_config['json_schema_extra'])['$id'])
		file_name = Path(url.rsplit('/', 1)[-1])
		file_path = output_dir / file_name
		with open(file_path, 'w', encoding='utf8') as f:
			json.dump(clazz.model_json_schema(), f, indent=2, ensure_ascii=False)
		print('Generated', file_path)

	generate(MCDReforgedConfig)
	generate(PermissionConfigModel)
	generate(PluginMetadataJsonModel)
	generate(LinkedDirectoryPluginJsonModel)


if __name__ == '__main__':
	main()
