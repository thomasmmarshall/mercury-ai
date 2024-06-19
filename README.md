# Advanced AI Assistant  

## Getting Started
To begin your journey with, make sure Python is installed on your system. Follow these steps to set up and start engaging with your data in a whole new way:

### Installation

1. Clone the Mercury repository:
   ```bash
   git clone https:/github.com/thomasmmarshall/mercury-rag
   ```
2. Navigate to the Mercury directory:
   ```bash
   cd Mercury
   ```
3. Install the required dependencies:
   ```
   poetry install
   ```
4. Activate the environment:
   ```bash
   poetry shell
   ```

### Configuration

Create a `secrets.json` file in the `/app/` directory with your OpenAI and Azure credentials to enable the advanced NLP features:

```json
{
    "OPENAI_API_KEY": "your-openai-api-key"
}
```

### Usage - Running Locally

Run with the following command inside of the Poetry shell:

```bash
python -m chainlit run app/main.py
```

This will launch the app in your browser, where you can start your data dialogue with.

## License
This repo is available under the GNU GPL v3 License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, please file an issue in the repository's issue tracker.

Embark on a data conversation journey with and experience the future of data interaction today!

Contact me at marshallthomasm@gmail.com

## Notes
I did not write the implementation of RAPTOR contained in this repo, this is from https://github.com/langchain-ai/langchain/blob/master/cookbook/RAPTOR.ipynb.
