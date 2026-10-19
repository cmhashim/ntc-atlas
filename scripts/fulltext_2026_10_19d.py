"""Task 23 (2026-10-19): full-text extraction for 12 abstract-only papers (2023–2024).
Same pipeline as Tasks 21–22: one model per paper (MODEL), verbatim quote per value, Claude checked quotes and
numbers against corpus/ PDFs. Fields already tied to a full-text or curator record are not overwritten."""

MODEL = {
 "trafficaugmentation": "Codex",
 "cilbenchmark": "Codex",
 "replication": "Codex",
 "genericmae": "GLM",
 "ptu": "GLM",
 "memento": "Codex",
 "crossembeddings": "Gemini",
 "expmd": "Gemini",
 "pragmatic": "Gemini",
 "jewel": "Mistral",
 "netgpt": "Mistral",
 "rosetta": "Mistral"
}

# Catalogued collections each paper names in its full text, with that paper's own locator.
DATASETS = {
 "trafficaugmentation": [
  [
   "mirage19",
   "mirage22"
  ],
  "Section 4.1; Table 4"
 ],
 "cilbenchmark": [
  [
   "mirage19"
  ],
  "Section V-B"
 ],
 "replication": [
  [
   "ucdavis",
   "mirage19",
   "mirage22",
   "utmobile"
  ],
  "Section 3.4; Table 2"
 ],
 "jewel": [
  [
   "iot23"
  ],
  "Section IV-C"
 ],
 "netgpt": [
  [
   "iscxvpn",
   "ustc"
  ],
  "Section 4.1; Table 1"
 ],
 "rosetta": [
  [
   "iscxvpn"
  ],
  "Section 3.1.1"
 ],
 "pragmatic": [
  [
   "ctu13",
   "cicids2017"
  ],
  "Section 6.1; Table 4"
 ],
 "ptu": [
  [
   "iscxvpn",
   "ustc",
   "cstnet",
   "ciciot2022",
   "crossplatform"
  ],
  "Section IV-A"
 ],
 "genericmae": [
  [
   "mirage19",
   "iscxvpn"
  ],
  "Section 4; Table 3"
 ],
 "memento": [
  [
   "mirage19"
  ],
  "Section 4.1"
 ]
}


def extract(detail, P, D=()):
    url = {p["id"]: p["url"] for p in P}
    for p in P:
        if p["id"] in DATASETS:
            p["datasets"] = list(dict.fromkeys(p["datasets"] + DATASETS[p["id"]][0]))
    for d in D:
        d["papers"] = [p["id"] for p in P if d["id"] in p["datasets"]]
    detail('cilbenchmark', {
        "Traffic unit definition": "The traffic unit is a bidirectional flow defined by the transport protocol, source and destination IP addresses, and source and destination ports. (Section V-B, footnote 10)",
        "Input representation": "Each input is a single-channel matrix containing time series of transport-layer payload size, inter-arrival time, direction and TCP window size. (Sections V-B and V-C)",
        "Packets / bytes": "Each sample uses the first 10 payload-carrying packets of a biflow, with zero padding for shorter biflows. (Section V-B)",
        "Preprocessing / anonymisation": "Zero-payload packets are discarded; direction is encoded as upstream or downstream, and the TCP window field is set to zero for UDP packets. (Section V-B; footnote 12)",
        "Architecture": "The shared backbone has two two-dimensional convolutional layers with 32 and 64 filters of size 4 × 2, each followed by max pooling and batch normalisation. Flattened features feed a fully connected layer of size 200 and an approach-specific output head. (Section V-C; Figure 8)",
        "Parameters": "The reference architecture has approximately 540k trainable parameters. (Section V-C)",
        "Fine-tuning objective": "The authors' iCaRL+ variant combines a classification cross-entropy term over old and new classes with a knowledge-distillation term, and uses the native model head for inference. (Section IV-D; Equations 12 and 17)",
        "Training / evaluation datasets": "Evaluation uses MIRAGE19 with 40 Android applications from 16 app-market categories and approximately 100k labelled biflows. (Section V-B)",
        "Metrics": "Metrics are macro F1, DropAll, DropOld and DropNew relative to training from scratch, and Forgetting relative to the best previous performance on old tasks. (Section V-A; Equations 20–22)",
        "Reported results": "The benchmark finds that BiC and OvA-Ens both exceed 73% macro F1 in the 39 + 1 scenario. High intransigence remains unresolved, with the best reported DropNew still 41.9% in that scenario. (Sections VI-A and VI-E)",
        "Hardware": "Controlled timing uses one core of an Intel Core i7-4710MQ CPU at 2.50 GHz with 11.6 GB RAM; an additional comparison uses an NVIDIA Tesla T4 cluster. (Section VI-D, footnote 18)",
        "Memory": "Exemplar rehearsal normally uses 1k samples; the memory-sensitivity experiment tests budgets of 100, 1k, 10k and 100k samples. (Section V-D; Section VI-C)",
        "Measurement scope": "Efficiency measurements cover CPU process time for model updates, including pre-SGD, SGD and post-SGD operations, and are averaged across runs relative to training from scratch. (Section VI-D; Figure 14; footnotes 18–19)",
        "Deployment limitations": "OvA-Ens and LUCIR require specially trained base models and cannot extend a conventionally trained classifier. Small increments continue to suffer high intransigence, while the training cost of model-growth approaches limits their use with large increments. (Section VII)",
        "Evaluation setting": "FACIL compares LwF, iCaRL, EWC, EEIL, IL2M, LUCIR, BiC and SSIL with iCaRL+, OvA-Ens and six fine-tuning/freezing baselines. Single increments use 20 + 20 and 39 + 1 scenarios; sequential increments start from 20 or 34 applications, with random application orders and a shared CNN backbone. (Sections II, IV, V-C and V-D)"
}, url['cilbenchmark'], "Full text; field locators in each value")
    detail('crossembeddings', {
        "Traffic unit definition": "Packets arriving at darknet or honeypot sensors grouped by destination TCP or UDP port, preserving the sequence of sender hosts contacting each port within a daily window. (Section III-B)",
        "Input representation": "Continuous vector embeddings in e-dimensional space learned for each host IP address, which serve as inputs to the downstream classifier or aligner neural network. (Section III-B)",
        "Packets / bytes": "Filtering retains only active hosts that sent at least 5 packets within the one-day collection batch. (Section V-B)",
        "Preprocessing / anonymisation": "Hosts sending fewer than 5 packets per day are filtered out, and in the honeypot scenario, only TCP-SYN packets are extracted. (Section V-B; Section VII-C)",
        "Architecture": "The alignment model is a DNN with 3 hidden layers of 1,024 units each with input layer normalisation and linear or Sigmoid activations. The downstream classifier is a feed-forward DNN with two hidden layers of 512 and 256 ReLU units, 30% dropout, and a softmax output layer. (Section IV-B; Section V-C)",
        "Pretraining objective": "Word2Vec context prediction trained in a self-supervised masked fashion to predict context hosts within a context window cw given a target host in the sequence. (Section III-B)",
        "Pretraining datasets": "Host embeddings are pretrained on 31 days (December 2022) of packet-level traffic from /24 darknets or 32 days of honeypot traffic. (Section V-B; Section VII-C)",
        "Fine-tuning objective": "The aligner DNN is trained to minimise mean squared error between mapped anchor host embeddings, while the downstream classifier minimises categorical cross-entropy using Adam. (Section IV-B; Section V-C)",
        "Training / evaluation datasets": "Two /24 darknet sensors in different autonomous systems and geographic regions captured over 43 days (1 Dec 2022 to 11 Jan 2023) across 10 ground-truth scanner/botnet classes plus unknown, and a 42-day TPOT low-interaction honeypot deployment covering 13 classes. (Section V-B; Section VII-B)",
        "Split strategy": "Five-fold stratified cross-validation split across provider and customer hosts, structured so that common anchor hosts remain in the same fold; models are trained on 4 provider folds, validated on the 5th provider fold, and tested on the 5th customer fold. (Section VI)",
        "Metrics": "Macro-averaged precision, recall, and F1-score for supervised classification, and silhouette and homogeneity for unsupervised clustering. (Section VI; Section VIII-A)",
        "Reported results": "Darknet, both networks with 32 days (Table III): F1 0.92 for canonical transfer (precision 0.94, recall 0.92) and for non-linear alignment (0.96, 0.90), against 0.95 for the independent reference. With 1 customer day (Table II) transfer keeps F1 0.92 against 0.81 for the reference. Honeypot to darknet (Table IV): transfer F1 0.86 (precision and recall 0.88), non-linear alignment 0.80, independent reference 0.81. (Section VI; Tables II–IV)",
        "Hardware": "An Nvidia Tesla V100-PCIE-16GB GPU. (Section V-C)",
        "Latency": "Per-day i-DarkVec 1-epoch update required 1.7 s on darknet traffic and 23 s on honeypot traffic; per-fold classifier and aligner training averaged 24 s and 60 s to 69 s respectively. (Section V-C; Section VII-C)",
        "Measurement scope": "Efficiency measurements encompass the average daily training and update times of i-DarkVec, as well as per-fold training runtimes of the classifier and aligner networks. (Section V-C)",
        "Deployment limitations": "The framework requires a non-empty subset of common active senders (anchors) across networks to enable alignment or context transfer, as well as administrative agreements and distribution systems. (Section IV-A; Section VI-C; Section IV-D)"
}, url['crossembeddings'], "Full text; field locators in each value")
    detail('expmd', {
        "Traffic unit definition": "Flow defined by 5-tuple (source IP, destination IP, source port, destination port, and protocol), encompassing both upload and download directions. (Section III)",
        "Input representation": "Four domains: metadata features (packet counts, byte counts, flow duration), byte-distribution domain (concatenated 256-dimensional byte frequency vectors for upload and download), textual domain (raw byte sequences mapped via byte embeddings), and temporal domain (signed packet lengths mapped to [-MTU, +MTU] and converted via an embedding layer). (Section III; Section IV-A to IV-D)",
        "Packets / bytes": "First 784 bytes of upload payload and first 784 bytes of download payload, padded with [PAD] when shorter; packet lengths capped at MTU of 1500. (Section IV-C; Section IV-D)",
        "Architecture": "ExpMD ensembles four sub-models via soft voting: Meta-RF (Random Forest), BD-boost (XGBoost on 512-dimensional vector), Text-Net (byte embedding, 1D-CNN pooling, L-layer residual blocks for upload and download processed separately and merged via MLP), and PS-Net (bidirectional multi-layer RNN over packet-length embeddings merged via MLP). (Section IV-A to IV-E; Fig. 1; Fig. 2; Fig. 3)",
        "Fine-tuning objective": "Cross-entropy loss for Text-Net; weighted multi-task objective combining cross-entropy loss and Triplet loss for PS-Net. (Section IV-C; Section IV-D)",
        "Training / evaluation datasets": "NUDT_MobileTraffic dataset, using 104 selected applications divided into a training dataset and a testing dataset. (Section V)",
        "Metrics": "Accuracy, macro-F1, and class counts/percentages exceeding specified F1 score thresholds. (Section V-A; Table II; Table III)",
        "Reported results": "ExpMD achieves an accuracy of 0.9755 (97.5%) and macro-F1 of 0.9756 across 104 applications. Sub-models achieve: Meta-RF (accuracy 0.8927, macro-F1 0.8921), BD-boost (accuracy 0.9103, macro-F1 0.9111), Text-Net (accuracy 0.9508, macro-F1 0.9517), and PS-Net (accuracy 0.9053, macro-F1 0.9055). (Abstract; Section V-A; Table II)",
        "Hardware": "Server with Intel Xeon Gold 5222 CPU @ 3.80GHz, NVIDIA GeForce GTX 3090 GPU, and 128GB of RAM. (Section V)",
        "Deployment limitations": "Removal or obfuscation of plaintext initial handshake metadata (such as TLS SNI) significantly degrades textual-domain performance, byte-distribution features offer limited signal under uniform encryption payloads, and behavioral features in metadata and temporal domains carry higher risk of confusion across similar behaviors. (Section VI)"
}, url['expmd'], "Full text; field locators in each value")
    detail('genericmae', {
        "Traffic unit definition": "Samples are TCP/UDP flows for T1 (MIRAGE) and T3 (ISCX) and sender IP addresses for T2 (DARKNET); flow samples use sequences of packet inter-arrival times, lengths and TCP receiver window values, with the first k = 32 measurements in T3. (Section 3.1; Sections 4.1-4.3)",
        "Input representation": "Bi-modal inputs: entities (server IP addresses, ports, /24 subnets) are embedded with Word2Vec skip-gram, while quantities are adapted per type: flow statistics through a fully connected layer, sequences of quantities through a 1D-CNN, and raw payload bytes through an embedding layer followed by a GRU, each projecting to an l1-dimensional space. (Section 1; Sections 3.2.1-3.2.2)",
        "Packets / bytes": "T1 flows carry up to 32 bytes of application payload; T3 flows use the first 32 bytes of payload plus statistics from TCP payload; T2 keeps only senders that sent at least five packets in one month. (Sections 4.1-4.3)",
        "Preprocessing / anonymisation": "MIRAGE background traffic is filtered out in post-processing; ISCX is restricted to non-tunnelled traffic; the DARKNET unknown class is ignored during validation, following the original authors; no IP or port masking is described. (Sections 4.1-4.3; Section 5.1)",
        "Architecture": "Per-input-type adaptation modules (Word2Vec for entities, FC for statistics, 1D-CNN for sequences, embedding layer plus GRU for payload) feed a symmetric five-layer autoencoder integration module (l2, l3, l4, l3, l2 neurons) whose l4-neuron layer yields the embedding E(s); the downstream classifier is a fully connected feed-forward network with two hidden layers (512 and 256 neurons), 30% dropout, ReLU and Softmax. (Sections 3.2-3.3; Section 5.1)",
        "Parameters": "Integration module hidden sizes are fixed at l2 = 512 and l3 = 256 after a coarse grid search, with l4 = 64 (T1) and l1 in [50, 200] for entity embeddings; downstream classifiers need 17 × 10^4 trainable parameters with MAE embeddings versus 29 × 10^4 (T1), 33 × 10^4 (T2) and 28 × 10^4 (T3) with raw concatenation. (Section 5.1; Section 5.2; Section 3.2.1; Table 4)",
        "Pretraining objective": "Self-supervised reconstruction: the MAE (quantities adaptation modules plus integration module) is trained to minimise a weighted Mean Squared Error reconstruction loss with linear decoder activations; Word2Vec entity embeddings are trained separately with skip-gram, predicting context membership within a window of n words. (Section 3.2.1; Section 3.3)",
        "Fine-tuning objective": "Supervised downstream traffic classification on frozen MAE embeddings: a fully connected classifier is trained with class-balanced categorical cross-entropy and an Adam optimiser. (Section 5.1)",
        "Training / evaluation datasets": "T1: MIRAGE-2019, 44k mobile-app flows, 16 classes, balance 0.94; T2: DARKNET, one month to a /24 darknet, 14k sender IP addresses (5k from known classes), 13 classes plus one unknown, balance 0.4; T3: ISCXVPN2016 non-tunnelled flows, 609 samples, 5 classes, balance 0.82. (Section 4; Table 3)",
        "Split strategy": "Five-fold cross-validation per task with average statistics reported; stratified sampling for T1 and T3 keeps flows from the same application session on one side of the split; the unknown class is ignored for T2. (Section 5.1)",
        "Metrics": "Macro average F1-Score and weighted average F1-Score for classification, plus the macro-averaged K-NN class probability pC(K) with cosine distance to gauge embedding neighbourhood purity. (Section 5.2; Section 7.1; Table 4)",
        "Reported results": "MAE embeddings score 0.87 macro and 0.88 weighted F1 on MIRAGE, 0.98 macro and 1.00 weighted on DARKNET, and 0.68 macro and 0.75 weighted on ISCX, versus 0.89/0.90, 0.98/0.99 and 0.66/0.74 with raw concatenation. Ablations show MAE matches or improves on any single measurement (best individual: 0.82 IP embeddings on T1, 0.98 statistics on T2), and shallow learners on T1 reach 0.86 (RF) and 0.83 (7-NN) macro F1 against the DNN's 0.87. (Table 4; Table 5; Section 8)",
        "Measurement scope": "The only efficiency-related figure is the number of trainable parameters of downstream classifiers, used as a proxy for training cost; no throughput, latency, memory or FLOPs measurements are reported. (Section 5.2)",
        "Deployment limitations": "Alternative adaptation and integration architectures (e.g. GNN embeddings) remain untested, and more use cases and datasets are still to be explored. Drift and temporal or spatial generalisation are not investigated, the changing traffic mix alters observable entities and quantities, and privacy-improving techniques and protocols would affect the MAE representations. (Section 9)",
        "Leakage / shortcut risks": "Session-level leakage is mitigated for T1 and T3: stratified sampling guarantees flows belonging to the same application session appear only in training or only in testing. (Section 5.1)",
        "Version notes": "Internal inconsistency: the ISCX IP-address-only macro F1 is 0.46 in the Section 6 text but 0.47 in Table 5; Table 4 omits the T3 reference score because only a fraction of the original ISCX dataset is used. (Section 6; Table 5; Table 4)"
}, url['genericmae'], "Full text; field locators in each value")
    detail('jewel', {
        "Traffic unit definition": "Joint packet-level and flow-level inference; early packets (1 to n-1) classified individually, packet n triggers flow-level classification. (Abstract; Section III-A)",
        "Input representation": "Packet-level (PL) and flow-level (FL) features; PL from packet headers, FL from flow state such as inter-arrival times. (Section I; Section III-B)",
        "Preprocessing / anonymisation": "Traffic filtering identifies target flows and extracts PL features from relevant headers. (Section III-A)",
        "Architecture": "Single Random Forest model performing both packet and flow classification. (Abstract; Section III-B)",
        "Training / evaluation datasets": "UNIBS (service classification), UNSW-IoT (device identification), IoT-23 (malicious traffic detection), ToN-IoT (cyberattack detection). (Section IV-C; Figure 5)",
        "Split strategy": "Time-ordered temporal splits. (Section IV-C)",
        "Metrics": "F1 score with micro, macro, and weighted averaging; per-packet evaluation. (Section IV-D)",
        "Reported results": "2.0–5.3% F1 accuracy gain over second-ranked benchmarks; 3.2% higher average F1 than second-best across all scenarios. (Abstract; Section V)",
        "Hardware": "Edgecore Wedge 100BF-QS switches with Intel Tofino BFNT10-032Q chipsets, 32×100GbE QSFP28 ports; Intel SDE 9.7.0; servers with Intel 8-core Xeon @2GHz, 48GB RAM. (Section IV-A)",
        "Throughput": "Line-rate inference with concurrent 100 Gbps background traffic. (Section IV-A)",
        "Latency": "Nanosecond-level inference latency. (Section I)",
        "Memory": "Constrained by PISA architecture memory limits for TCAM, register actions, and range match tables. (Section III-C)",
        "Measurement scope": "F1 classification accuracy and TCAM resource usage. (Section V)",
        "Deployment limitations": "Flow tracking register collisions prevent flow-level inference, fallback to packet-level only. (Section III-A)"
}, url['jewel'], "Full text; field locators in each value")
    detail('memento', {
        "Traffic unit definition": "A biflow is a bidirectional flow identified by source and destination IP addresses and ports plus transport protocol, allowing source and destination to be swapped. (Section 4.1, footnote 2)",
        "Input representation": "Per-packet time series contain transport-layer payload size, inter-arrival time, TCP window size and direction for MIRAGE19; CESNET-TLS22 uses payload size, inter-arrival time and direction because window size is unavailable. (Section 4.1, per-packet properties paragraph)",
        "Packets / bytes": "Each sample uses the first 10 packets with non-zero payload; shorter sequences are padded with zeros. (Section 4.1, final paragraph)",
        "Preprocessing / anonymisation": "Zero-payload packets are excluded, direction is encoded by upstream or downstream sign, and UDP window size is set to zero. Memory augmentation applies Gaussian jittering and translation to inter-arrival times. (Sections 4.1 and 3.1.2)",
        "Architecture": "A 2D-CNN has two convolutional layers followed by pooling and normalisation operations and a dense output layer. The backbone structure stays unchanged while the head expands to accommodate newly added classes. (Section 4.2)",
        "Fine-tuning objective": "Incremental training combines categorical cross-entropy classification with knowledge distillation from the previous episode, using selective smoothing of teacher responses for new-app samples. A separate correction stage optimises categorical cross-entropy with the main model frozen. (Sections 3.2.1 and 3.3, Equations (1)–(4))",
        "Training / evaluation datasets": "MIRAGE19 contains 40 Android app classes; CESNET-TLS22-40 and CESNET-TLS22-80 retain the 40 and 80 most represented services, respectively. CESNET subsets randomly retain 0.15% of biflows per class. (Section 4.1; Tables 4–6 and 8)",
        "Split strategy": "For balanced incremental validation, stored memory biflows are divided into 90% training and 10% validation, with equal validation counts per class across old and new apps. (Section 3.2.2)",
        "Metrics": "Macro F1 and balanced accuracy, defined as mean per-class recall, are reported separately for all, old and new classes. Derived measures are the drop from a model trained from scratch and Maximum Improvement Over the Best Baseline. (Section 4.4, Equations (8)–(11))",
        "Reported results": "For 39+1, overall macro F1 drops from training from scratch are 2.24 ± 1.02 percentage points on MIRAGE19 and 1.49 ± 0.72 on CESNET-TLS22-40; for 20+20 they are 8.59 ± 1.54 and 6.62 ± 0.66, respectively. On CESNET-TLS22-80, overall drops are 1.34 ± 0.52 for 79+1, 5.87 ± 0.60 for 40+40, and 12.50 ± 0.95 at the final episode of 20+20+20+20. (Tables 4–6 and 8, MEMENTO rows, F1 Score Drop All columns)",
        "Hardware": "Experiments used a machine with two Intel Xeon Gold 6252N CPUs at 2.30 GHz and 378 GB memory; execution-time measurements used a single CPU core. (Section 4; Section 5.1, footnote 5)",
        "Measurement scope": "Efficiency measurements cover incremental training and post-training herding, using sequential CPU process time in an otherwise idle environment. Table 7 reports training-time reductions against training from scratch, rather than inference performance. (Section 5.1, footnote 5; Section 6.5; Table 7)",
        "Deployment limitations": "The performance gap against ideal training from scratch remains. Evaluation in network environments different from training and adaptation to intra-class concept drift are left for future work. (Section 7, final paragraph)",
        "Leakage / shortcut risks": "To keep augmented samples within their source partition, each original memory biflow and all its synthetic derivatives are assigned together to training or validation. (Section 6.1, small-increment configuration)",
        "Version notes": "Section 6.5 claims greater than 90% training-time gain across all datasets in the small-increment scenario, but Table 7 reports 89.38% for MIRAGE19 at 39+1. The classification-loss weight is also inconsistent: Section 4.3 specifies the old-class fraction, whereas Section 5.2 specifies the new-class fraction. (Sections 4.3, 5.2 and 6.5; Table 7)"
}, url['memento'], "Full text; field locators in each value")
    detail('netgpt', {
        "Traffic unit definition": "traffic denotes both packets and flows. (Section 3)",
        "Input representation": "bytes to hex tokens via tokeniser. (Section 3.1)",
        "Packets / bytes": "max token size 512; first three packets for long flows. (Section 4.1)",
        "Preprocessing / anonymisation": "headers removed during pretraining. (Section 4.1)",
        "Architecture": "GPT-2 auto-regressive Transformer. (Section 3.1)",
        "Parameters": "GPT-2-base with 0.1B parameters. (Section 4.1)",
        "Pretraining objective": "auto-regressive next token prediction. (Section 3.1)",
        "Pretraining datasets": "ISXW, DoHBrw, USTCTFC, PrivII (Cybermine excluded). (Table 1; Section 4.1)",
        "Fine-tuning objective": "traffic understanding reformulated as generation with prompts. (Section 3.2)",
        "Training / evaluation datasets": "five datasets: ISXW, DoHBrw, USTCTFC, PrivII, Cybermine with eight tasks. (Table 1; Section 4.1)",
        "Split strategy": "5000 packets for validation, 5000 for testing, rest for pretraining. (Section 4.1)",
        "Metrics": "Accuracy, Macro F1, Jensen-Shannon Divergence; higher AC/F1 better, lower JSD better. (Section 4.1)",
        "Reported results": "Generation: NetGPT and GPT-2 reach JSD around 0.1; NetGPT has the best average and lowers JSD on ISXW by about 50% relative to GPT-2. (Section 4.3; Table 3)",
        "Hardware": "V100-32GB GPUs. (Section 4.1)",
        "Deployment limitations": "small model; datasets not large enough to cover all traffic types. (Section 5)",
        "Evaluation setting": "compared with ET-BERT and GPT-2 on packet and flow levels. (Section 4.1)"
}, url['netgpt'], "Full text; field locators in each value")
    detail('pragmatic', {
        "Traffic unit definition": "Traffic is represented as high-level NetFlow records summarizing communications between two endpoints. (Section 2.1; Appendix A.1)",
        "Input representation": "Models take either a Complete feature set using all features generated by the respective flow exporter, or an Essential feature set consisting of approximately half the features including basic flow metadata. (Section D.4)",
        "Preprocessing / anonymisation": "Plain IP addresses and network ports are removed to prevent shortcut learning, with ports converted to their corresponding IANA category. (Section D.4)",
        "Architecture": "Six pipeline designs are evaluated (binary BD, multiclass MD, binary-to-multiclass cascade BMD, and ensembles ED-o, ED-v, ED-s) across four classification algorithms: Decision Trees, Random Forests, Logistic Regression, and Histogram Gradient Boosting. (Section 6.1; Section D.6)",
        "Training / evaluation datasets": "Five flow datasets are used: CTU13 (Argus), NB15 (Zeek), UF-NB15 (nProbe), CICIDS17 (FlowMeter fixed version), and GTCS (FlowMeter). (Section 6.1; Table 4)",
        "Split strategy": "The test set E is composed of 20% of samples per class randomly chosen from the dataset D. Training set T evaluates four availability levels (80%, 40%, 15%, or 100 samples per class) over 100 to 1,000 random trials for static evaluation, plus a chronological split using the initial samples for training and the final 20% for testing. (Section 6.1; Section D.3)",
        "Metrics": "Evaluation measures true positive rate (tpr), false positive rate (fpr), training and testing runtimes, and accuracy (Acc) calculated exclusively on malicious classes for multiclass setups. (Section E.3)",
        "Hardware": "Evaluations span six platforms: an Intel Xeon W-2195 with 36 cores and 256 GB RAM, an Intel Core i7-10750HQ workstation with 32 GB RAM, an Intel Core i5-4670 desktop with 8 GB RAM, an Intel Core i5-430M laptop with 8 GB RAM, a 4-core 8 GB RAM downclocked virtual machine, and a Raspberry Pi 4B with 2 GB RAM. (Section D.2)",
        "Measurement scope": "Runtime covers standalone training duration on partition T and complete batch inference duration across all samples in test partition E. (Section E.3)",
        "Deployment limitations": "Key operational hurdles identified by the authors include the uniqueness and dynamic evolution of individual networks, the presence of adaptive adversaries, and the difficulty of interpreting complex machine learning decisions. (Section 3.2; Section 7.1)",
        "Evaluation setting": "The benchmark evaluates four machine learning algorithms across six architectural detector pipelines, two feature sets, five datasets, four data budget regimes, and both static and temporal splits under known, unknown, and adversarial attack scenarios. (Section 6.1)",
        "Leakage / shortcut risks": "To eliminate experimental bias and shortcut artefacts, the authors stripped IP addresses and replaced raw ports with IANA functional categories, addressed sample composition skew, and tested time-ordered splits. (Section D.3; Section D.4)",
        "Version notes": "Section 6.1 lists scarce training data availability as 20% of D, whereas Section D.3 specifies it as 15% of D (one fifth of the non-test remainder). (Section 6.1; Section D.3)"
}, url['pragmatic'], "Full text; field locators in each value")
    detail('ptu', {
        "Traffic unit definition": "Packet-level: the packet is the input unit and downstream tasks run at the granularity of individual packets, with temporal context drawn from the packet's session flow, the bidirectional stream sharing the protocol, IP and port quintuple. (Section II-A)",
        "Input representation": "Packet bytes are segmented into 16-bit tokens (vocabulary 2^16 = 65536), while session inter-arrival times normalised by sigmoid(log10(inter-arrival)) form temporal tokens; the modified embedding layer sums token, position, packet and time embeddings, with independent lookup tables for packet versus temporal tokens and [CLS]/[PKT] separators. (Sections II-A, III-B)",
        "Packets / bytes": "Each sample is one packet truncated to Ni = 128 tokens with at most Nt = 10 appended temporal tokens; pre-training inputs concatenate two packets, and the input sequence length for all experiments is set to 256 bytes. (Sections II-B, III-B, IV-E)",
        "Preprocessing / anonymisation": "IP addresses, MAC addresses and the checksum field are removed from the otherwise retained network and transport headers to prevent the model learning harmful biases from strong identification fields. (Section II-A)",
        "Architecture": "Standard BERT backbone with 12 attention heads, 12 layers and 768-dimensional token embeddings; downstream tasks add only a task-specific output layer on the [CLS] token's output vector. (Sections III-A, III-B)",
        "Pretraining objective": "Four self-supervised targets, Masked Packet Reconstruction, Same Session Prediction, Historical Interval Prediction and Future Interval Prediction, whose losses are summed as the overall pre-training loss. Best settings: Pmasked = 20, Pmask = 80, Prandom = 10, Pnext = 30, Psession = 30, Ptime = 50, run with batch size 32 for 500,000 steps over about five days. (Sections II-B, III-B)",
        "Pretraining datasets": "Approximately 100GB of unlabeled traffic from public datasets [34] and [35], covering QUIC, TLS, FTP, HTTP, SSH and other protocols, both encrypted and plaintext, with no overlap with the labelled evaluation datasets; one shared pre-trained checkpoint serves all downstream tasks. (Section III-B)",
        "Fine-tuning objective": "Supervised fine-tuning of the whole pre-trained model on task-specific labelled data, at most 5000 samples per class, with batch size 32 for 10 epochs (about 3 to 10 hours), adding only a task-specific output layer on the [CLS] vector. (Sections III-A, III-B)",
        "Training / evaluation datasets": "Traffic classification: ISCX-VPN-2016 (application and service), USTC-TFC-2016 (malware), CSTNET-TLS-1.3 (encrypted application), CIC-IoT-2022 (attack) and Cross-Platform iOS and Android (mobile apps). QoE inference: CC-YouTube-QoE-2018 (buffer, resolution, state) plus KoNViD-1k and LIVE Netflix for MOS, where inputs are built from video metadata and features in 100ms slices as in LSTM-QoE. (Section IV-A)",
        "Split strategy": "Per task, training, validation and test sets are divided 8:1:1; the few-shot analysis deviates from this and varies the training proportion from 10% to 90% in 10% increments. (Sections III-B, IV-D)",
        "Metrics": "Accuracy and F1 score, macro-averaged over classes to avoid imbalance bias, for traffic and QoE classification tasks; PLCC and SRCC between predicted and actual MOS sequences for the two MOS inference tasks. (Section IV-A)",
        "Reported results": "PTU is SOTA on all tasks: traffic classification AC and F1 above 0.99 on all six datasets (CSTNET-TLS-1.3 AC 0.9945/F1 0.9940; CIC-IoT-2022 AC 0.9947/F1 0.9942), QoE classification AC 0.9274, 0.9493 and 0.8597 on CC-Buffer, CC-Resolution and CC-State, and MOS PLCC 0.9429 (KoNViD-1k) and 0.9608 (LIVE Netflix). Without pre-training, CSTNET-TLS-1.3 accuracy falls to 0.9132, and PTU stays above 90% accuracy even with 10% of the training data. (Tables II-V; Section IV-D)",
        "Hardware": "All experiments ran on a server with NVIDIA GeForce RTX 3090 GPUs, four for pre-training and a single GPU for fine-tuning; implementation uses Uer-py and PyTorch 2.1.2. (Section III-B)",
        "Throughput": "Offline batch inference: about 200 samples per second at batch size 1 with 256-byte inputs, and approximately 3000 samples per second at batch size 32 (the experimental default); linear attention could add a further 3 to 4 times speed-up but degrades performance. (Section IV-E)",
        "Latency": "An additional delay of approximately 5 ms per flow, which the authors call non-negligible. (Section VI)",
        "Measurement scope": "The efficiency numbers cover offline batch inference on an RTX 3090 with 256-byte inputs at batch sizes 1 and 32 only; they do not cover live core-network operation, which the authors state PTU cannot yet meet. (Sections IV-E, VI)",
        "Deployment limitations": "The authors state the roughly 2000 samples per second inference speed lags the core network requirement of tens of millions of packets per second, that the 5 ms per-flow delay is non-negligible, and that applying PTU to the real-world core network is still challenging. (Section VI)",
        "Leakage / shortcut risks": "IP and MAC addresses are removed to prevent harmful biases from strong identification fields; the 'w IP' ablation shows retaining them costs only moderate accuracy because IP addresses correlate consistently with labels within each dataset's train and test subsets, a shortcut expected to cause more pronounced degradation in production. Pre-training and evaluation datasets are stated to have no overlap. (Sections II-A, III-B, IV-C)",
        "Version notes": "Section IV-E reports approximately 3000 samples per second at batch size 32 whereas Section VI reports approximately 2000 samples per second on a single consumer-grade GPU; Table V labels the MPR ablation row 'w/o MTM' while the text calls it 'w/o MPR'. (Sections IV-E, VI; Table V)"
}, url['ptu'], "Full text; field locators in each value")
    detail('replication', {
        "Traffic unit definition": "Flowpic samples summarise the first 15 seconds of a network flow. (Sections 2.2 and 4.2.1)",
        "Input representation": "Flowpics are two-dimensional histograms of packet size against time, without traffic direction; the study tests resolutions of 32 × 32, 64 × 64 and 1500 × 1500. The ML comparison also uses concatenated packet-size, direction and inter-arrival-time sequences. (Sections 2.2, 4.1.1 and 4.2.1; Table 4)",
        "Packets / bytes": "Flowpics bin packet sizes over the range 0–1500 within a 15-second observation window; the alternative ML representation uses the first 10 packets. (Sections 2.2 and 4.1.1)",
        "Preprocessing / anonymisation": "UCDAVIS19 is converted from CSV to Parquet without further filtering; the other datasets remove flows with fewer than 10 packets and classes with fewer than 100 samples. MIRAGE datasets additionally remove TCP ACK packets and background traffic, while the UTMOBILENET21 partitions are combined. (Section 3.4, Data curation)",
        "Architecture": "The study uses LeNet5 for mini-flowpics and a larger CNN for full-flowpics. SimCLR uses a feature extractor with a projection head, followed by a frozen representation and a trainable classification layer for few-shot fine-tuning. (Section 3.2; Appendix C, Listings 1–5)",
        "Parameters": "For five-class, 32 × 32 inputs, the supervised network has 61,281 parameters, SimCLR pretraining has 68,842 or 75,376 depending on projection size, and the fine-tuning architecture has 51,297. (Appendix C, Listings 1–5)",
        "Pretraining objective": "SimCLR uses the InfoNCE contrastive objective to pull augmented views of the same sample together and separate them from negative views. (Sections 2.4 and 3.2)",
        "Pretraining datasets": "SimCLR pretraining uses the UCDAVIS19 pretraining partition, initially sampled into balanced per-class subsets; an additional experiment enlarges training to the full pretraining partition. (Sections 3.4, 4 and 4.4.3)",
        "Fine-tuning objective": "A classifier layer is fine-tuned with a few labelled samples while the pretrained representation is frozen; augmentations are used only during pretraining. (Section 3.2, Training steps)",
        "Training / evaluation datasets": "The study uses UCDAVIS19 with five classes, MIRAGE19 with 20 classes, MIRAGE22 with nine classes and curated UTMOBILENET21 with 14 classes. MIRAGE22 is also evaluated with a longer-flow subset; ISCX-VPN and ISCX-Tor are excluded after preliminary investigation. (Section 3.4; Table 2)",
        "Split strategy": "UCDAVIS19 uses five non-overlapping groups of 100 flows per class from pretraining, each with repeated 80/20 training/validation splits, and evaluates on script, human and unused pretraining flows. Replication on the other datasets specifies an 80/10/10 training/validation/test split preserving class imbalance. (Sections 4.2.1 and 4.5.1)",
        "Metrics": "UCDAVIS19 evaluation reports accuracy with confidence intervals; replication on the imbalanced datasets uses F1, without a stated averaging convention. Augmentation ranks are compared with a post-hoc Nemenyi test. (Sections 4.1.1, 4.3 and 4.5.1)",
        "Hardware": "Experiments run on Linux servers equipped with multiple NVIDIA Tesla V100 GPUs. (Section 3.3)",
        "Memory": "For 32 × 32 inputs, architecture printouts estimate total memory of 0.36 MB for supervised learning, 0.39 MB for the smaller SimCLR projection, 0.42 MB for the larger projection and 0.33 MB for fine-tuning. (Appendix C, Listings 1–5)",
        "Measurement scope": "Memory figures are torchsummary architecture estimates; reported experiment durations describe modelling runs rather than packet-processing measurements. (Section 4.2.2; Appendix C, Listings 1–5)",
        "Deployment limitations": "Flowpics require observing multiple seconds of traffic, which can delay classification and limit their suitability for prioritisation, scheduling and shaping. (Section 2.2, Related work)",
        "Evaluation setting": "The reproduction compares supervised CNN training and SimCLR with few-shot fine-tuning across six augmentations and a no-augmentation control, with XGBoost as an ML reference. It adds ablations of resolution, dropout, projection size, augmentation pairs and training-set size, then replicates supervised augmentation comparisons on additional datasets. (Sections 3.1–3.3 and 4.1–4.5)",
        "Leakage / shortcut risks": "Inspection of the reference repository finds that its loader mixes UCDAVIS19 partitions and includes test flows in training; the authors also identify distribution shift in the human partition. They exclude ISCX datasets after noting insufficient viable flows and published concerns about exploitable dataset bias. (Section 3.4, Reproducibility; Section 4.2.3; Appendix D)",
        "Version notes": "The reference repository differs from the published architecture, activation functions, dropout and learning-rate scheduling, preventing faithful reproduction from that code. The original authors also clarified that they combined the pretraining and script partitions, whereas this study initially treated them separately. (Appendix D; Section 4.2.1, footnote 10)"
}, url['replication'], "Full text; field locators in each value")
    detail('rosetta', {
        "Traffic unit definition": "flow-level packet length sequences. (Section 3; Abstract)",
        "Input representation": "packet length sequences. (Section 2)",
        "Packets / bytes": "100 packets per sample, truncated or zero-padded. (Section 3.1.1; Appendix A)",
        "Preprocessing / anonymisation": "Reordering by timestamps, duplicate packet removal, IP address replacement. (Section 3.1.1)",
        "Architecture": "Two modules: TCP-aware traffic augmentation (five algorithms) and traffic invariant extractor (TIE) using BYOL with online and target networks. (Section 4.2-4.4)",
        "Pretraining datasets": "Third-party TLS dataset with 502,109 malicious and 613,419 benign flows, augmented to ~120 variants per flow. (Section 5.1)",
        "Fine-tuning objective": "Supervised traffic classification using TIE feature vectors and labels. (Section 4; Figure 4)",
        "Training / evaluation datasets": "CIRA-CIC-DoHBrw-2020 (249,750 malicious, 917,300 benign), ISCX-VPN (16,007 VPN, 22,716 non-VPN), real website flows (~1.8M), real application flows (292,523). (Section 3.1.1; Section 3.2.1)",
        "Split strategy": "flow-level 6:2:2 train:validation:test ratio. (Section 3.1.1)",
        "Metrics": "Accuracy and F1-score. (Section 3.1.2)",
        "Reported results": "Baseline: average accuracy drops by 2.9-42.62% and F1 by 3.27-58.09% across environments; with Rosetta: average F1 87.49% in θ0-θ6. (Section 3.1.2; Table 2; Section 5.5; Table 9)",
        "Hardware": "GeForce RTX 2080 GPU. (Section 5.1)",
        "Deployment limitations": "Requires changing input layer dimension to match Rosetta feature size; slight accuracy drop in similar environments. (Section 4.2; Section 6)",
        "Evaluation setting": "Six DL models (DF, FS-Net, Transformer, SDAE, CNN, LSTM) tested across diverse network environments. (Section 3)",
        "Leakage / shortcut risks": "Packet length sequences change due to TCP mechanisms: subsequence shift, duplication, and size variation. (Section 3.3)"
}, url['rosetta'], "Full text; field locators in each value")
    detail('trafficaugmentation', {
        "Traffic unit definition": "Each sample represents the first 20 packets of a flow, with zero padding at the tail where required. (Section 4.1, Data folds and normalization)",
        "Input representation": "A multivariate packet time series contains packet size, direction and inter-arrival time. (Section 4.1, Data folds and normalization)",
        "Packets / bytes": "The input budget is 20 packets per flow. (Section 3.1)",
        "Preprocessing / anonymisation": "MIRAGE-19 and MIRAGE-22 are curated to remove background traffic and flows with fewer than 10 packets; Enterprise requires no specific preprocessing. Packet sizes and inter-arrival times are clipped, inter-arrival times are logarithmically scaled, and features are normalised. (Section 4.1, Data curation; Data folds and normalization)",
        "Architecture": "A one-dimensional CNN uses a backbone with two ResNet blocks followed by a linear classification head. (Section 4.1, Model architecture and training; Figure 7)",
        "Parameters": "The MIRAGE-19 architecture has 115,028 parameters, all trainable. (Appendix, Listing 1.1)",
        "Training / evaluation datasets": "The benchmark uses MIRAGE-19 with 20 classes and 64k curated flows, MIRAGE-22 with nine classes and 26k curated flows, and the private Enterprise dataset with 100 classes and 2.9 million flows. (Section 4.1; Table 4)",
        "Split strategy": "The curated flow datasets are divided into 80 random train/validation/test splits with proportions 70/15/15; normalisation and augmentation statistics are extracted from the combined training and validation portions. (Section 4.1, Data folds and normalization)",
        "Metrics": "Classification is measured with weighted F1, reported as an average across 80 runs with confidence intervals. (Sections 4.1 and 5.1; Table 5)",
        "Reported results": "Translation improves weighted F1 by 4.40 ± 0.13 points on MIRAGE-19, Wrap by 2.09 ± 0.08 points on MIRAGE-22, and Bernoulli Mask by 1.25 ± 0.16 points on Enterprise. Combining augmentations with MaskedStack reaches a 4.63 ± 0.14-point improvement on MIRAGE-19. (Section 5.1, Table 5; Section 5.4, Table 7)",
        "Hardware": "Experiments run on Linux servers equipped with multiple NVIDIA Tesla V100 GPUs. (Section 4.1, Model architecture and training)",
        "Memory": "The MIRAGE-19 architecture printout estimates 0.44 MB for parameters, 0.09 MB for the forward/backward pass and 0.53 MB in total. (Appendix, Listing 1.1)",
        "Measurement scope": "Memory figures are architecture-printout estimates covering the input, parameters and forward/backward pass. (Appendix, Listing 1.1)",
        "Deployment limitations": "Increasing augmentation injection can make the performance gain too small relative to the computational cost. (Section 5.2, Batching policies)",
        "Evaluation setting": "The CNN benchmark compares 18 augmentation functions from amplitude, masking and sequence families, including individual and combined transformations. It investigates augmentation magnitude, Replace/Inject/Pre-augment batching policies and class-weighted sampling against training without augmentation. (Sections 3.1–3.4, 4.1 and 5.1–5.4)",
        "Version notes": "A footnote describes a 256-dimensional latent space, but Listing 1.1 shows a 128-channel pooled representation feeding the 20-class linear layer (2,580 parameters). (Section 5.3, footnote 13; Appendix, Listing 1.1)"
}, url['trafficaugmentation'], "Full text; field locators in each value")
