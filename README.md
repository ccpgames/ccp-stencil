# CCP Stencil

An Alviss and Jinja2 powered template renderer where the context input can be 
files and entire directory structures can be rendered.

This is a generalized variant of the "CCP Borg Bootstrapper" project 
bootstrapping and build and deployment tool which used entire "template" 
projects that were rendered to bootstrap entire projects and to render CI/CD 
manifests on demand. 

The rest of this readme is (at the moment) just a "sketch" for how this package 
should work and was written before any actual code or functionality.

## Context

- [x] No context (Weird use case...?!?)
- [x] kwargs context (via code)
- [x] Dict context (via code)
- [x] Alviss file context (json/yaml + inheritance)
- [x] Args context (from commandline)

## Template

- [x] String template (via code)
- [x] File template
- [x] Args template (from commandline)
- [ ] Directory template

## Renderer

- [x] String renderer (via code)
- [x] Stdout renderer (for commandline)
- [x] File renderer
- [ ] Directory renderer

## Other features...?

- [x] ENV var rendering (can be done via ${__ENV__:FOO} in Alviss input)?
- [ ] Meta-data header in files for Directory rendering that controls file names and/or if they should be rendered or not
  - [x] Skip-if tag for skipping file rendering
  - [ ] Some meta-tag that can control the output name of a file via the `FileRenderer`
- [ ] Meta-data file for directories in Directory rendering that control the directory name?
- [x] Proper Jinja2 Environment Template Loader to enable Jinja's include/extend stuff?
- [x] Custom macros/scripts/filters?

## Use Cases

- From commandline (main use case, e.g. rendering CI/CD manifests)
- From code

### Command Line Use Case Examples

Using these as a basis for functionality (this is written before any actual code)!

#### Example 1

```shell
$ ccp-stencil -i context.yaml -t template.html -o result.html
```

- Alviss file input: `-i context.yaml`
- Template file input: `-t template.html`
- Render file output: `-o result.html`


#### Example 2

```shell
$ ccp-stencil -a name=Bob -a age=7 -a color=Red -s "My name is {{name}} and I am {{age}} years old and my favorite color is {{color}}"
My name is Bob and I am 7 years old and my favorite color is Red
```

- Args input: `-a name=Bob -a age=7 -a color=Red`
- String template input: `-s "My name is {name} and I am {age} years old and my favorite color is {color}"`
- Print (stdout) output: _No argument, this is default!_


#### Example 3

```shell
$ ccp-stencil -T templates/ -O build/
```

- No context input: _No argument, this is default!_
- Template directory input: `-T templates/`
- Render directory output: `-O build/`