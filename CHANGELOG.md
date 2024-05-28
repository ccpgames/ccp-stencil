# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.2.0] - 2024-05-28

Embedding Extension & Base64 Filter update

### Added

- The `EmbedExtension` to the Jinja2 environment used that enables using the 
  `{% embed 'my_file.txt' %}` to embed the requested file "as-is" (so not 
  parsed as a template or anything like that) into templates wholesale with 
  these optional arguments:
  - `indent` (default: 0) to indent each line of the embedded file by a certain
    number of spaces, e.g. for embedding into YAML files, where indent is 
    syntactically important
  - `alviss` (default: `False`) to run the embedded file though the Alviss 
    "render_loader" before embedding the results
  - `env` (default: `False`) to make the Alviss parser render `${__ENV__:...}` 
    expressions
  - `fidelius` (default: `False`) to make the Alviss parser render 
    `${__FID__:...}` expressions
- The main use case here was considered things like creating Kubernetes File 
  Config maps where e.g. config file content is embedded wholesale into the 
  manifest's YAML
- The `base64` filter to the Jinja2 environment used to quicly encode context 
  variables as base64 encoded strings
  - The main use case here was considered things like rendering of Kubernetes 
    Secret manifests where keys need to be base64 encoded  
- A bunch of "proper" unittests for the new embedding and filter functions

### Changed

- The `FileTemplate` now uses the Jinja2 environment's `FileSystemLoader`, 
  pre-seeded with search paths of the current working directory (`os.getcwd()`) 
  as well as the root directory of the script being executed (`sys.argv[0]`) 
  plus whatever paths are defined in the `STENCIL_TEMPLATE_PATH` environment 
  variable, if any (multiple paths seperated by `;`)


## [0.1.0] - 2024-05-24

Initial release

### Added

- The project in its entirety
- Template types:
  - `FileTemplate`
  - `StringTemplate`
- Context types:
  - `DictContext`
  - `KeyWordArgumentContext`
  - `AlvissContext`
- Renderer Types
  - `StringRenderer`
  - `StdOutRenderer`
  - `FileRenderer`
