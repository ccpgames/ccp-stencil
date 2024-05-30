# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [0.5.0] - 2024-05-30

## Changed

- Bumped the version requirement of Alviss to 3.3 to get support for the new 
  `${__PY__:...}` expressions in order to inject module versions into Alviss 
  contexts for CI/CD manifests


## [0.4.0] - 2024-05-30

### Added

- New Extension that adds a `{% skip_if %}` tag where you can insert any 
  condition (e.g. checking the Context) and if it evals as True, a 
  `CancelRendering` exception is raised and caught by the Renderers causing 
  them to silently just skip rendering that template.
  - The `StringRenderer` returns `None`
  - The `StoutRenderer` prints out nothing
  - The `FileRenderer` doesn't create an output file
- Added unittests for the `{% skip_if %}` tag


## [0.3.0] - 2024-05-28

### Fixed

- A bug in the `guess_template_by_argument` method that raised exceptions while 
  checking to see if a given string could be interpreted as a path to an 
  existing file (which should be allowed to fail silently and then the string 
  returned as a `StringTemplate`)


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
- A "shortcut" method called `render_stencil` for quicly rendering to `str` (via
  the `StringRenderer`) in code that takes two simple kwargs called `template` 
  and `context` and will use the appropriate Template and Context 
  implementations based on the type and/or value of those arguments (see below)
- Two utility functions that attempt to instantiate the appropriate Template and 
  Context types based on the argument types supplied as `template` and 
  `context`:
  - A template that is an instance of `pathlib.Path` will be a `FileTemplate`
  - A template that is a multi-line `str` will be a `StringTemplate`
  - A template that is a single-line `str` will:
    - First attempt to see if it refers to a template name that Jinja2 can load, 
      and return a `FileTemplate` if so
    - Then it'll see if the string can be interpreted as a file system path to a 
      file that exists, and then return a `FileTemplate`
    - If all that fails, it'll just assume the `str` is the template itself and 
      return a `StringTemplate`
  - A context that is an instance of `pathlib.Path` or a `str` will be an 
    `AlvissContext`
  - A context that is a `dict` will be a `DictContext`
- A bunch of "proper" unittests for the new embedding and filter functions

### Changed

- The `FileTemplate` now uses the Jinja2 environment's `FileSystemLoader`, 
  pre-seeded with search paths of the current working directory (`os.getcwd()`) 
  as well as the root directory of the script being executed (`sys.argv[0]`) 
  plus whatever paths are defined in the `STENCIL_TEMPLATE_PATH` environment 
  variable, if any (multiple paths seperated by `;`)
  - This change enables and vastly simplifies using the Jinaj2 built in 
    expressions like `{% extends ... %}` and `{% include ... %}` "out of the 
    box" so to speak as well as making custom `{% marcro ... %}` files to 
    include.


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
