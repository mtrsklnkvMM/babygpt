<h1 align="center">
 babyagi

</h1>

# Objective

This README will cover the following:

* [How the script works](#how-it-works)

* [How to use the script](#how-to-use)

* [Supported Models](#supported-models)

# How It Works<a name="how-it-works"></a>


# How to Use<a name="how-to-use"></a>
To use the script, you will need to follow these steps:

1. Clone the repository via `git clone https://github.com/yoheinakajima/babyagi.git` and `cd` into the cloned repository.
2. Install the required packages: `pip install -r requirements.txt`
3. Copy the .env.example file to .env: `cp .env.example .env`. This is where you will set the following variables.

All optional values above can also be specified on the command line.

# Supported Models<a name="supported-models"></a>

This script works with all OpenAI models, as well as Llama through Llama.cpp. Default model is **gpt-3.5-turbo**. To use a different model, specify it through OPENAI_API_MODEL or use the command line.

## Llama

Download the latest version of [Llama.cpp](https://github.com/ggerganov/llama.cpp) and follow instructions to make it. You will also need the Llama model weights.

 - **Under no circumstances share IPFS, magnet links, or any other links to model downloads anywhere in this repository, including in issues, discussions or pull requests. They will be immediately deleted.**

After that link `llama/main` to llama.cpp/main and `models` to the folder where you have the Llama model weights. Then run the script with `OPENAI_API_MODEL=llama` or `-l` argument.
