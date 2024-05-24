from ccpstencil import stencils


def main():
    # ctx = stencils.DictContext()
    # ctx = stencils.DictContext({'name': 'Bob', 'age': 7, 'color': 'Red'})
    # ctx = stencils.KeyWordArgumentContext(name='Bob', age=7, color='Red')
    ctx = stencils.AlvissContext('_sandbox_input.yaml')

    # tpl = stencils.StringTemplate('My name is {{name}} and I am {{age}} years old and my favorite color is {{color}}')
    tpl = stencils.FileTemplate('_sandbox_template.txt')

    # rnd = stencils.StringRenderer(ctx, tpl)
    # rnd = stencils.StdOutRenderer(ctx, tpl)
    rnd = stencils.FileRenderer('./build/something/_sandbox_output.txt', ctx, tpl, overwrite=True)
    print(rnd.render())


if __name__ == '__main__':
    main()
