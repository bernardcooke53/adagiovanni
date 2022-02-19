# Assumptions
There is no UI currently required though this would help bring the product to life. The MVP is purely a
backend REST API, and Giovanni is a capable enough user of `cURL` and Python's `requests` library to
work with this in the initial phase.

The MVP for the product needs to accept sandwich orders and list outstanding tasks for Giovanni.
Another assumption is that Giovanni stocks certain ingredients for a fixed choice of sandwiches on the menu,
and that customers can choose from any of the available sandwiches. A sample of common sandwich choices is
included, but that may need to be customised by Giovanni at a later date.

The MVP doesn't include any scope for customization of sandwich orders.
The MVP doesn't allow customers to edit or cancel their order after submission!
The MVP makes Giovanni's schedule public - if Giovanni wants to put his schedule into an admin portal,
this can be added in a later iteration.

Based on Giovanni's input, customers will place their order for pickup ASAP and the schedule will reflect
the earliest time it can be served on a first-come, first-served basis. This means if Stavros places his order
now, and Anisa 10 seconds later, Stavros' order will be added to the schedule immediately for pickup in 2.5 minutes.
Anisa's order will be added to the schedule for pickup 3.5 minutes after Stavros' is scheduled for service, to allow
Giovanni time to serve and take payment for Stavros' order, and prepare Anisa's.

Customers will pay in-person upon service of their sandwich, and through separate software (this doesn't have any payment
integration!).
