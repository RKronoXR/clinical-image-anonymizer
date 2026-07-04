# Clinical Image Anonymizer

Local-first tool for anonymizing common clinical image files.

Status: early development.

## License

Clinical Image Anonymizer is distributed under the **ACTA AI Lab Attribution License v1.0**.

You may copy, use, modify, publish, distribute, sublicense, and sell copies of the software, provided that attribution to the original project is preserved.

Required attribution:

- Project: Clinical Image Anonymizer
- Author: Ricardo Eugenio Gonzalez Valenzuela
- Organization: ACTA AI Lab
- Repository: https://github.com/RKronoXR/clinical-image-anonymizer

See [`LICENSE`](../LICENSE) for the full license text.

## Citation

If you use Clinical Image Anonymizer for research, teaching, datasets, reports, presentations, theses, preprints, or publications, please cite the project.

Recommended acknowledgement:

> This work used Clinical Image Anonymizer v1.0.0, developed by Ricardo Eugenio Gonzalez Valenzuela at ACTA AI Lab, for local-first clinical image anonymization.

Citation metadata is available in [`CITATION.cff`](../CITATION.cff).

## Disclaimer

Clinical Image Anonymizer is a research prototype.

It is not a medical device, not a clinical tool, not for diagnosis, and not for clinical decision-making.

Users remain responsible for verifying that every exported image is sufficiently anonymized before sharing, publishing, uploading, or using it in research.

See [`DISCLAIMER.md`](../DISCLAIMER.md) for the full disclaimer.

## REST API

The project includes a local-first FastAPI REST API.

Start locally:

```powershell
python -m uvicorn src.api.app:app --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000/docs
```

See [`docs/rest_api.md`](docs/rest_api.md) for endpoint details, examples, localhost/LAN usage, and privacy guidance.