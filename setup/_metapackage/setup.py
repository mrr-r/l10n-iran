import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-l10n-iran",
    description="Meta package for oca-l10n-iran Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-l10n_ir_accounting',
        'odoo14-addon-l10n_ir_base',
        'odoo14-addon-l10n_ir_hr_contract',
        'odoo14-addon-l10n_ir_states',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
