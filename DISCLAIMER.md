# Disclaimer

## Research Prototype

Clinical Image Anonymizer is a research prototype developed for local-first clinical image anonymization workflows.

It is intended for research, teaching, demonstration, internal academic workflows, and software engineering portfolio use.

## Non-Clinical Tool

Clinical Image Anonymizer is not a clinical tool.

It must not be used for diagnosis, treatment planning, clinical decision-making, patient management, or any other direct clinical purpose.

## Not a Medical Device

Clinical Image Anonymizer is not a certified, approved, or regulated medical device.

It has not been validated, certified, or approved for clinical use by any regulatory authority.

## No Diagnostic Function

Clinical Image Anonymizer does not provide diagnosis, prediction, detection of disease, treatment advice, risk scoring, clinical interpretation, or medical recommendations.

The software only supports image anonymization workflows by:

- inspecting available image metadata;
- removing or reducing supported metadata where possible;
- applying user-defined rectangular pixel censoring to output copies;
- exporting anonymized copies to a selected output location.

## User Responsibility

The user remains fully responsible for verifying that every exported image is sufficiently anonymized before storing, sharing, publishing, uploading, or using it in research.

This includes checking:

- metadata;
- file names;
- visible labels;
- burned-in annotations;
- patient names;
- patient IDs;
- dates of birth;
- institutional identifiers;
- any other direct or indirect identifying information.

Automatic verification, metadata inspection, and manual censoring support are helpful safeguards, but they do not replace careful human review.

## Original Images

Original images remain the property of their original owners, institutions, patients, or data controllers.

Clinical Image Anonymizer must not be used to claim ownership over images, datasets, annotations, metadata, or derived files that belong to others.

## Original File Safety

Clinical Image Anonymizer is designed to preserve original files.

The software should not modify, move, crop, overwrite, rename, delete, or replace original input images.

The anonymization workflow should write new output copies to a selected output location.

Users should still keep backups and verify outputs before deleting or moving any source material.

## Local-First Processing

Clinical Image Anonymizer is designed as a local-first tool.

By default, images should be processed locally on the user's computer.

Users should not upload non-anonymized clinical images, private images, sensitive datasets, or generated outputs to public services, remote servers, GitHub, or other platforms unless they have explicit permission and have completed the required privacy review.

## Sensitive and Medical Data

Clinical images and image metadata may contain sensitive personal data.

Users are responsible for following applicable institutional, legal, ethical, privacy, and data-protection requirements.

This may include local institutional policies, research ethics approvals, GDPR requirements, data processing agreements, and project-specific data governance rules.

## No Warranty

Clinical Image Anonymizer is provided without warranty.

The software is provided "as is", without guarantees of completeness, accuracy, fitness for a particular purpose, clinical safety, regulatory compliance, or perfect anonymization.

The authors and contributors are not responsible for privacy breaches, data loss, misuse, clinical use, regulatory non-compliance, or decisions made based on this software.

## Recommended Safe Use

Before sharing exported images, users should:

1. verify that original files were not modified;
2. inspect exported files visually;
3. inspect metadata where possible;
4. confirm that visible identifiers were censored;
5. confirm that file names do not contain identifying information;
6. keep private data out of GitHub and public repositories;
7. document the anonymization workflow used in the research project.

## Project Information

- Project: Clinical Image Anonymizer
- Version: 1.0.0
- Author: Ricardo Eugenio Gonzalez Valenzuela
- Organization: ACTA AI Lab
- Repository: https://github.com/RKronoXR/clinical-image-anonymizer
