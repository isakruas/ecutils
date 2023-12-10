# Contributing to ECUtils

Thank you for your interest in contributing to the ECUtils project, our dedicated toolkit for Elliptic Curve Cryptography. Your effort is highly valued, and we aim to ensure that your contribution process is seamless and rewarding. Please follow the guidelines outlined below to make a successful contribution to the project.

## Setting Up Your Development Environment

The first step in contributing is to set up your local development environment:

1. Fork the ECUtils repository on GitHub.
2. Clone your fork to your local development machine.
3. Change to the project directory:

   ```bash
   cd ecutils
   ```

4. Install the project in editable mode with its development dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

By working in editable mode, any changes you make will be reflected without the need for reinstallation.

## Making Changes and Using Prefixes

When you're ready to start making changes:

1. Create a branch with a prefix that indicates the purpose of your changes:

   ```bash
   # Use the appropriate prefix: feature/, fix/, doc/, test/, refactor/, or style/
   git checkout -b feature/name-of-your-feature
   ```

2. Adhere to the coding conventions and best practices found throughout the project while making your changes.

## Writing and Running Tests

It's essential that your contributions are well-tested:

1. Place your new tests in the `tests` directory, ensuring they're appropriately named to match the related feature or fix.

2. Aim for high test coverage to maintain the robustness of ECUtils:

   ```bash
   pytest --cov=ecutils tests/
   ```

Ensure that your contributions pass all tests and that the overall test coverage isn’t compromised.

## Submitting Pull Requests (PRs)

To submit your changes for review:

1. Push your contributions to your forked repository.
2. In the 'ECUtils' original repository, initiate a 'New pull request'.
3. Choose your fork and the branch where your changes were made.
4. Clearly title your PR using the same prefix as your branch, followed by a concise description:

   ```plaintext
   Feature: Implement new elliptic curve model
   Fix: Resolve point addition edge case
   Doc: Update README with contribution guidelines
   Test: Add tests for point doubling
   Refactor: Refine internal structure for module X
   Style: Adjust code formatting for consistency
   ```

5. In your PR's description, explain your changes and note any issues addressed using the format `fixes #issue_number`.
6. Submit the pull request.

## Code Review and Integration Process

Expect a review from the project's maintainers, who will assess the changes, run further tests, and perhaps suggest enhancements before integrating your code. Stay involved by responding to any feedback or inquiries regarding your submitted PR.

## Acknowledgment

We deeply appreciate your contributions to the ECUtils project. Your dedication to enhancing this toolkit doesn't go unnoticed. Together, we can continue to develop this vital resource for the cryptography community.

Transfer your ideas into action—let's collaborate to elevate ECUtils to new heights!