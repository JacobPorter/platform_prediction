# platform_prediction
Predict sequencing platform.
The models may need to be un-gzipped to be used.
Requirements in platform_environment.yml. (scikit-learn, scipy, etc.)
The specific version of scikit-learn may be required to use the models since scikit-learn may not be backwards compatible.

To create an executeable run make in the directory of this program.

Test case:
./predict_platform ./test/SRR8776902.5k.nanopore.fastq.gz ./test/SRR12594727.5k.illumina.fastq.gz

Jacob S. Porter, PhD
https://github.com/JacobPorter/
