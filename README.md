# Nelo payment acquirer for Odoo

An implementation of the [Odoo Payment Acquirer](https://www.odoo.com/documentation/user/14.0/general/payment_acquirers/payment_acquirers.html) module for Nelo payments.

## Installation

To install the Nelo add on, run the following command from the Odoo root directory:

`git submodule add https://github.com/nelo/odoo-payment-acquirer addons/payment_nelo`

This will install the Nelo payment acquirer code as a submodule in your Odoo project. You can commit the directory and the `.gitmodules` file to your codebase. Git will recognize the directory as a submodule and will not track its contents in your git history. Instead, to update the submodule at any time, simply run `git submodule update --remote` from you root directory.

More information on how git submodules work can be found [here](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

## Branches for old Odoo versions
In major versions, Odoo may introduce breaking changes for addon providers. To accomodate customers on various versions of Odoo, Nelo publishes branches for recent major versions.

To target a specific Odoo version, specify the branch when adding Nelo's submodule. As an example, to target Odoo v12:

`git submodule add -b odoo-12.0 https://github.com/nelo/odoo-payment-acquirer addons/payment_nelo`

## Configuration

Once the submodule is installed you can run the server as normal and follow [these](https://www.odoo.com/documentation/user/14.0/general/payment_acquirers/payment_acquirers.html#configuration) instructions for configuring Nelo on your e-commerce site.
