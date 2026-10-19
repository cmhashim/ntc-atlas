"""Task 24 (2026-10-19): full-text extraction for the last 25 abstract-only papers (2005–2023).
Same pipeline as Tasks 21–23, split by model reliability (Codex for table-heavy papers, GLM for short ones): one model per paper (MODEL), verbatim quote per value, Claude checked quotes and
numbers against corpus/ PDFs. Fields already tied to a full-text or curator record are not overwritten."""

MODEL = {
 "acdc": "Codex",
 "nprint": "Codex",
 "deeppacket": "Codex",
 "appscanner": "Codex",
 "bayes": "Codex",
 "early": "Codex",
 "dpi": "Codex",
 "distiller": "Codex",
 "dodont": "Codex",
 "flowprint": "Codex",
 "commercial": "Codex",
 "miniflowpic": "Codex",
 "vpnfeatures": "Codex",
 "evs2vec": "GLM",
 "deepmal": "GLM",
 "cicissues": "GLM",
 "torfeatures": "GLM",
 "flowrest": "Gemini",
 "refinery": "Gemini",
 "manyfew": "Gemini",
 "survey": "Gemini",
 "tfegnn": "Mistral",
 "fsnet": "Mistral",
 "mimetic": "Mistral",
 "blinc": "Mistral"
}

# Catalogued collections each paper names in its full text, with that paper's own locator.
DATASETS = {
 "tfegnn": [
  [
   "iscxvpn",
   "iscxtor"
  ],
  "Section 4.1.1"
 ],
 "miniflowpic": [
  [
   "ucdavis"
  ],
  "Section 3.1.1"
 ],
 "deepmal": [
  [
   "ustc",
   "ctu13"
  ],
  "Section IV-A"
 ],
 "cicissues": [
  [
   "cicids2017"
  ],
  "Section II"
 ],
 "torfeatures": [
  [
   "iscxvpn"
  ],
  "Section 4"
 ],
 "flowrest": [
  [
   "cicids2017"
  ],
  "Section IV-B"
 ],
 "refinery": [
  [
   "cicids2017"
  ],
  "Section 5.2.2"
 ],
 "manyfew": [
  [
   "mirage19"
  ],
  "Section V-A; Table III"
 ],
 "nprint": [
  [
   "cicids2017",
   "crossplatform"
  ],
  "Table 1"
 ],
 "distiller": [
  [
   "iscxvpn"
  ],
  "Section 4.1; Table 3"
 ]
}


def extract(detail, P, D=()):
    url = {p["id"]: p["url"] for p in P}
    for p in P:
        if p["id"] in DATASETS:
            p["datasets"] = list(dict.fromkeys(p["datasets"] + DATASETS[p["id"]][0]))
    for d in D:
        d["papers"] = [p["id"] for p in P if d["id"] in p["datasets"]]
    detail('acdc', {
        "Traffic unit definition": "Application identification uses flows separated by source and destination IP addresses, source and destination ports, and protocol. (Sections 2.1 and 4.1, Dataset)",
        "Input representation": "nPrint encodes selected packet header fields as normalised binary features while preserving packet semantics. (Section 3.2, Preliminary Feature Selection)",
        "Packets / bytes": "Only header fields from the first three packets of each flow are used. (Section 3.2, Preliminary Feature Selection)",
        "Preprocessing / anonymisation": "The implementation removes payloads and both endpoints' IP addresses and ports; dataset preparation uses DNS queries to identify relevant application traffic before flow separation. (Section 3.2, Preliminary Feature Selection; Section 4.1, Dataset)",
        "Architecture": "An adaptive scheduler selects a LightGBM classifier and batch size from a pool generated using heuristic feature exploration. Evaluation uses 90 classifiers, with feature subset sizes from one to nine and 10 combinations per size. (Section 3.2, Classifier Generation; Section 3.4; Section 4.2)",
        "Training / evaluation datasets": "A curated TLS-encrypted dataset covers ten applications across video streaming, video conferencing and social media. Table 2 lists Netflix, YouTube, Amazon, Twitch, MS Teams, Google Meet, Zoom, Facebook, Twitter and Instagram. (Section 4.1, Dataset; Table 2)",
        "Split strategy": "Flows are divided equally between training and testing; traffic rates are emulated by randomly sampling flows from the test set. (Section 2.2; Section 4.2)",
        "Metrics": "Evaluation uses weighted F1-score, time-to-decision and memory requirements; classification throughput is derived from traffic rate divided by time-to-decision. (Section 2.2; Section 3.1; Section 4.1, Classification Throughput)",
        "Reported results": "Without a memory constraint and with minimum required F1-score set to 0.85, AC-DC achieves mean F1-score 0.855, maximum 0.869 and minimum 0.853 on the curated application dataset. (Section 4.2; Table 3, AC-DC row)",
        "Hardware": "Experiments use an AMD EPYC 7502P processor with 32 cores and 64 threads; classifiers distribute work across available cores. (Section 4.1, Testbed Setup)",
        "Throughput": "Under no memory constraint, AC-DC matches incoming traffic rates across the evaluated range of 100 to 15,000 flows/second. This throughput measures preprocessing and inference after raw feature extraction, using emulated traffic rates. (Sections 4.1 and 4.2; Figure 3)",
        "Latency": "Mean time-to-decision is 0.235 seconds without a memory constraint, covering feature preprocessing through completion of inference for the collected flows. (Section 3.1, Time-to-Decision; Table 3, AC-DC row, Avg. TTD column)",
        "Memory": "Memory requirements are the minimum combined RAM and swap needed for normal execution, aggregated across concurrent classifier instances. As one concrete pool entry, Table 6 reports 315 MB per instance for the classifier using IPv4 DF-bit, TCP FIN, IPv4 TTL and TCP ACK-flag at a batch size of 500 flows. (Section 3.1, Memory Requirement; Table 6, first classifier row)",
        "Measurement scope": "Time-to-decision includes intermediate I/O and classifier switching, but excludes raw feature extraction; unnecessary logging and metadata storage are removed. (Section 3.1, Time-to-Decision)",
        "Leakage / shortcut risks": "The authors remove endpoint addresses and ports because these fields may cause overfitting. (Section 3.2, Preliminary Feature Selection)",
        "Version notes": "Section 3.2 gives 32 features after preliminary selection but later discusses all 33 features. (Section 3.2; Section 4.2)"
}, url['acdc'], "Full text; field locators in each value")
    detail('appscanner', {
        "Traffic unit definition": "A flow groups bidirectional packets sharing a remote IP address and port within a burst; bursts end after a one-second inter-packet gap. Flows are distinct from TCP sessions, which may span multiple bursts. (Section 3.1, Definitions; Section 3.3, Traffic Burstification and Flow Separation)",
        "Input representation": "Models use either packet-length vectors with incoming lengths made negative or statistical features derived separately from incoming, outgoing and combined packet series. Statistical features are min-max scaled and selected using random-forest Gini importance. (Section 4, Classifier Design; Figure 2)",
        "Packets / bytes": "Evaluation accepts flows containing 7 to 260 packets and rejects flows outside these bounds. Statistical approaches use 40 selected features from an initial 54. (Section 5.1; Table 1)",
        "Preprocessing / anonymisation": "Training traces are filtered to error-free TCP traffic, and Network Log attribution removes traffic from other apps. Addresses are used for flow separation rather than identification, and packet payloads are excluded from features. (Sections 3.2 and 3.3; Section 3.4, TCP Pre-processing and Flow Classification)",
        "Architecture": "Six approaches combine SVC or random forests with classifiers per flow length, a single multiclass classifier, or a binary classifier per app. The single large random forest uses 150 trees, while each per-app random forest uses 10 trees. (Section 4; Table 1)",
        "Training / evaluation datasets": "The authors collect interactive traffic for 110 apps randomly chosen from the Google Play Store's top 150 free apps in July 2015. The accepted dataset contains 131,736 flows, with each app exercised for 75 minutes. (Section 5, System Evaluation; Section 5.1; Appendix Table 9)",
        "Split strategy": "Accepted flows are split into 75% training and 25% testing; exhaustive hyperparameter searches for the multiclass approaches use five-fold cross-validation. (Section 5.1; Section 4, Approaches 1 to 4)",
        "Metrics": "Metrics are precision, recall, accuracy and the percentage of flows classified after confidence filtering. Multiclass accuracy is the fraction of correct classifications, whereas binary accuracy includes true negatives. (Section 5.1; Section 5.2; Tables 4 and 5)",
        "Reported results": "Without confidence filtering, per-app random forests achieve 96.0% precision, 82.5% recall and 99.8% binary accuracy. At a prediction threshold of 0.9, the single large random forest achieves 99.7% precision, 99.6% recall and 99.6% accuracy while classifying 72.0% of flows. (Table 4, Per App Random Forest row; Table 5, Single Large Random Forest rows, 0.9 column)",
        "Hardware": "Traffic collection uses a Motorola XT1039 Moto G running Android KitKat, a Linksys E1700 access point and a Dell Optiplex workstation with two network interfaces. (Section 5, System Evaluation)",
        "Parameters": "Table 2 reports classifier sizes of 1 MB for each per-flow SVC or random forest, 350 MB for the large SVC, 180 MB for the large random forest, 35 MB for a per-app SVC and 4 MB for a per-app random forest. (Table 2, Size of classifier row)",
        "Measurement scope": "Reported efficiency characteristics concern training duration and classifier size; the real-time pipeline waits for the burst threshold before processing a burst. (Table 2; Section 3.4, Online Mode)",
        "Deployment limitations": "Shared advertisement, analytics and standard-API flows can be ambiguous without additional features. Training and testing use one device, and the authors caution that device, Android-version and TCP-implementation differences may cause misclassification. (Section 5.3; Section 6.1, Limitations)"
}, url['appscanner'], "Full text; field locators in each value")
    detail('bayes', {
        "Traffic unit definition": "Complete TCP connections identified by endpoint IP addresses, transport protocol and endpoint ports; connection establishment and termination must be observed. (Section 3.1 and footnote 2)",
        "Input representation": "Header-derived per-flow discriminators describe both directions, including duration, ports, inter-arrival times, payload sizes, effective bandwidth and Fourier transforms. (Section 3.1; Table 1)",
        "Preprocessing / anonymisation": "Source and destination IP addresses are excluded from classification, and the training and testing data are restricted to complete TCP connections. (Section 3.1 and footnotes 2–3)",
        "Architecture": "Naïve Bayes is evaluated with Gaussian density assumptions, Gaussian-kernel density estimation, FCBF discriminator selection, and their combination. (Sections 4.2–4.4 and 5.5)",
        "Training / evaluation datasets": "Hand-classified Genome Campus traffic contains 377526 flows across the categories listed in Table 2; INTERACTIVE and GAMES have insufficient data for accurate analysis. A separate evaluation uses traffic collected at the same site later. (Sections 3, 3.2, 5.1 and 6; Tables 2 and 4)",
        "Split strategy": "Time blocks are sampled across the day, with each block used for training in turn and tested against the remaining blocks. A separate later-time dataset tests temporal stability. (Section 5.1, Analysis Data; Section 6)",
        "Metrics": "Flow accuracy is the proportion of correctly classified flows, trust is the per-class probability that an assigned label is correct, and byte accuracy is the proportion of correctly classified flow bytes. (Section 5.1, Evaluation Criteria)",
        "Memory": "WEKA can load approximately 25000 instances with 132 discriminators in 128M, or 24500–25000 instances with 265 discriminators in 256M. (Section 5.1, Analysis Tools; Table 5)",
        "Measurement scope": "The timing experiment combines model construction and testing rather than measuring individual prediction latency. The memory figures describe the number of instances loadable into WEKA. (Section 5.1, Analysis Tools; Figure 5; Table 5)",
        "Deployment limitations": "The authors identify independence between flows as a limitation of the object model and leave evaluation across different network locations to future work. (Section 8, Future Work)",
        "Version notes": "Section 3.1 specifies 248 per-flow discriminators, whereas the WEKA memory table reports configurations with 132 and 265 discriminators. (Section 3.1; Table 5)"
}, url['bayes'], "Full text; field locators in each value")
    detail('blinc', {
        "Traffic unit definition": "Flows defined as 5-tuple (source/destination IP address, source/destination port, protocol) with 64-second idle timeout. (Section III-A)",
        "Input representation": "Flow records without packet timing or size information. (Section IV)",
        "Preprocessing / anonymisation": "No access to packet payload; no port number assumptions; only flow collector data. (Abstract)",
        "Architecture": "Multilevel approach with social, functional, and application levels. (Abstract; Section IV)",
        "Fine-tuning objective": "Balance accuracy versus completeness through adjustable classification thresholds. (Abstract)",
        "Training / evaluation datasets": "Three real traces: GN (Genome campus), UN1 and UN2 (residential university) from 2003-2004. (Section III-A; Table I)",
        "Metrics": "Completeness (ratio of classified flows/bytes) and accuracy (percentage of correctly labeled classified traffic). (Section V)",
        "Reported results": "80%-90% of flows classified with >95% accuracy; UN traces: >90% completeness at ~95% accuracy; GN: ~80% at 99% accuracy. (Abstract; Section V)",
        "Hardware": "DELL PE2850 with Xeon 3.4GHz processor and 2GB RAM. (Section VI-A)",
        "Memory": "Maximum memory usage under 40% of available 2GB. (Section VI-A)",
        "Deployment limitations": "Cannot identify specific application sub-types; fails if layer-3 headers encrypted; may require modification for NATs. (Section VI-B)",
        "Version notes": "Values read from the technical report; the atlas cites the SIGCOMM 2005 paper, so locators may differ. (corpus/blinc.pdf)"
}, url['blinc'], "Full text; field locators in each value")
    detail('cicissues', {
        "Traffic unit definition": "Flow-level: a bidirectional exchange of packets sharing one connection tuple (source and destination IPs, ports, transport protocol) within a time period; the dataset's flow timeout is 120 seconds, with flows also closed when the connection closes. (Section III-A)",
        "Input representation": "Flow-level statistical features computed with CICFlowMeter; each flow becomes one CSV row with 83 features excluding the label. (Sections III-A, III-D)",
        "Preprocessing / anonymisation": "Dataset regenerated from the original PCAPs with a corrected CICFlowMeter: TCP appendices are reunited with their head flows, RST packets correctly terminate flows, and a payload filter relabels attack flows lacking forward data transfer as 'X Attempted'; more than 20 percent of original traces are reconstructed or relabelled. (Abstract; Sections III-B2, IV-A)",
        "Architecture": "Random Forest classifier benchmarked on the original and corrected datasets, reported as the classifier with the best average F1-score. (Sections IV, IV-B)",
        "Fine-tuning objective": "Supervised multi-class flow classification: distinguish benign from malicious traffic and assign each attack to its attack class. (Section II (Labelling))",
        "Training / evaluation datasets": "CICIDS2017, regenerated from the original PCAPs into Original, Intermediate (TCP fixes) and Final (payload filter) versions; the public dataset comprises over 2.8 million traces in 15 classes, and the Final version adds an 'Attempted' category (Table I). (Section II; Table I; Section IV-A)",
        "Split strategy": "Train-test split of 75-25 on flows; all 'Attempted' flows are assigned to the BENIGN category for the experiments, with hyperparameters and random seeds in external documentation. (Section IV-B)",
        "Metrics": "Per-class precision, recall and F1-score plus accuracy and weighted averages; the authors deem aggregate-only metrics inadequate for this imbalanced dataset and recommend per-class metrics, confusion matrices and feature-importance analysis. (Section III-E; Table II)",
        "Reported results": "On the Final dataset the RF reaches weighted-average precision, recall and F1 of 0.99, with Bot F1 rising from 0.60 to 0.99, Web Brute Force from 0.77 to 0.95 and Web XSS from 0.18 to 0.79; Web Attack SQL stays at 0.00 F1 and several attack test sets are flagged as extremely small. (Section I; Table II)",
        "Deployment limitations": "The DoS Hulk class in CICIDS2017 cannot be used as intended because the deprecated tool renders the attack ineffective; the authors also note that results might differ based on the ML model used. (Section III-C1; Section IV-B)",
        "Evaluation setting": "Audit of the CICIDS2017 creation pipeline (attack simulation, flow construction, labelling, feature extraction, benchmarking); a Random Forest classifier is benchmarked on the three regenerated dataset versions under the revised per-class evaluation methodology. (Section II; Section IV-B)",
        "Leakage / shortcut risks": "TCP appendices form 25.9% of the dataset and let the RF overfit through shortcut learning on largely irrelevant features (Fwd Header Len, Total Fwd Pkt, Min Seg Size Fwd, Init Win bytes Fwd, SYN Flag Count, Bwd Pkt Len Mean). RST presence was a learned shortcut for Bot traffic, labelling relies solely on IPs and collection window, and attributes such as Flow ID, IPs, ports and Timestamp risk spurious class association. (Sections III-A1, III-B2, III-D, IV-B)"
}, url['cicissues'], "Full text; field locators in each value")
    detail('commercial', {
        "Traffic unit definition": "Samples are network flows identified by anonymised source/destination IP addresses, source/destination ports and transport protocol. (Section III, Dataset)",
        "Input representation": "Both CNN and XGBoost models consume one-dimensional time series of signed packet sizes, encoding size and direction and normalised by the network MTU. (Section IV-A2, Input)",
        "Packets / bytes": "Each model uses the first 100 TCP packets or first 10 UDP packets, represented by packet size and direction. (Section IV-A2, Input)",
        "Preprocessing / anonymisation": "IP addresses in collected flow logs are anonymised, and signed packet sizes are normalised using the MTU. The analysis discards the sparsely sampled application tail and retains applications with at least 100 flows for zero-day evaluation. (Sections III and III-3; Section IV-A2; Table III)",
        "Architecture": "Separate TCP/UDP CNNs use three convolutional layers with 32/16 filters of size 1×3, ReLU and max pooling, followed by fully connected layers of size 128/64 and SoftMax outputs of size 162/38. GradBP treats the predicted label as ground truth, computes a shadow backpropagation step without changing weights, and thresholds its gradient magnitude. (Section IV-A3; Figure 4; Section IV-B4, Equations 9–13)",
        "Training / evaluation datasets": "The private Huawei dataset contains approximately 10.5 million flows collected from four customer deployments over four weeks, with 3,231 application labels supplied by a commercial DPI engine. Known-traffic classification uses the top 200 applications, and zero-day evaluation adds 635 held-out application classes. (Section III; Tables III and IV; Section VI-B1)",
        "Split strategy": "CNN and XGBoost models are trained using the same dataset folds; zero-day applications are classes absent from supervised training. (Section IV-A6; Section IV-B)",
        "Metrics": "Known-application evaluation distinguishes flow-wise accuracy from application-wise accuracy, where each application counts equally. Zero-day evaluation uses ROC curves, TPR/FPR and TNR/FNR, plus flow and application detection at a fixed false-positive rate. (Section V-A; Figure 6; Section VI-A; Figures 9–12)",
        "Reported results": "Across the combined TCP/UDP zero-day evaluation, GradBP detects 79.2% of zero-day flows and 90.1% of zero-day application classes at FPR 1%. A class counts as detected when at least one of its flows is detected. (Section VI-B2; Figure 12)",
        "Hardware": "Zero-day detection cost measurements use TensorFlow v1.9 on an NVIDIA P100 GPU. (Section VI-D, Complexity)",
        "Throughput": "The unoptimised implementation reaches 100,000 zero-day detection function inferences per second. (Section VI-D, Complexity)",
        "Latency": "Both reported GradBP variants have an inference cost of 0.01 ms per sample and require no separate detector bootstrap. (Section VI-D; Table V, Gradient rows)",
        "Measurement scope": "The efficiency table measures bootstrap cost per dataset and inference cost per sample for the zero-day function g(x). Known-application model comparisons use parameter or tree-node counts as space complexity, which the authors caution does not directly determine execution time or energy expenditure. (Section IV-A5–IV-A6; Section V-C; Section VI-D; Table V)",
        "Evaluation setting": "Known-traffic experiments compare CNN and XGBoost using the same signed packet-size input and dataset folds, with separate TCP/UDP models. Zero-day experiments compare GradBP with input clustering, feature-vector clustering, SoftMax and OpenMax, calibrating rejection thresholds on known training traffic. (Sections IV-A and VI-A–VI-B)",
        "Leakage / shortcut risks": "The authors exclude inter-packet timing because it can encode endpoint distance rather than application behaviour. They also demonstrate that restricting class cardinality and reporting mean accuracy can conceal poor performance on less popular applications. (Section IV-A2; Section V-A1–V-A2; Figures 5 and 6)",
        "Deployment limitations": "Application evolution, scarce samples for new classes and environment-dependent traffic modes leave continuous, incremental and distributed learning as deployment challenges. Inference latency and explainability also require further work, and explainability is explicitly outside this study. (Section III-4; Section VII-4, Deployability)"
}, url['commercial'], "Full text; field locators in each value")
    detail('deepmal', {
        "Traffic unit definition": "Two units: packet-level, where each packet is one instance trimmed to its first n payload bytes, and flow-level, where the first m packets of a flow form one input (m = 2 packets, n = 100 bytes). (Section III-B; Table I; Fig. 1)",
        "Input representation": "Raw bytestream with no expert handcrafted features: every byte is decimal-normalised and used as a separate feature; packet inputs have shape (N, n) and flow inputs a tensor of size (N, m, n). (Section III; Fig. 1)",
        "Packets / bytes": "Raw Packets keep the first n = 1024 payload bytes per packet (one million packets in the first evaluation, 248,850 in the second); Raw Flows keep the first m = 2 packets per flow, each trimmed to n = 100 payload bytes (67,494 flows). (Section IV-A; Section IV-B; Table I)",
        "Preprocessing / anonymisation": "Potentially biasing bytes such as MAC and IP addresses are removed and the payload of each packet is taken as the key information; packets larger than n bytes are trimmed to the first n payload bytes and smaller ones are zero-padded at the end. (Section III; Section III-B)",
        "Architecture": "Raw Packets: two 1D-CNN layers (32 and 64 filters of size 5), max-pooling of size 8, an LSTM of 200 units returning full sequences, and two fully-connected layers of 200 units, plus batch-normalisation and dropout; the multi-class variant uses Softmax. Raw Flows: one 1D-CNN layer of 32 filters of size 5 and fully-connected layers of 50 and 100 units; built in Keras on TensorFlow. (Section III-A, III-C, III-D; Section IV-A; Section V; Figs. 2, 3)",
        "Fine-tuning objective": "No pretraining or fine-tuning: detection models are trained from scratch with binary cross-entropy loss, and the multi-class model with categorical cross-entropy behind a Softmax output layer. (Section III-C, III-D; Section V)",
        "Training / evaluation datasets": "Binary detection uses the USTCTFC2016 dataset from the CTU Stratosphere IPS Project (ten malware and ten benign traffic types, the latter generated with Ixia BreakingPoint); the second evaluation keeps the ten malware captures and adds sixteen normal capture types from CTU. Multi-class uses CTU botnet scenarios with four classes (Normal, Neris, Rbot, Virut). (Section IV-A, IV-B; Section V; Tables I, II)",
        "Split strategy": "Per-sample split with 80% of samples for training, 10% for validation and 10% for testing, applied to both packet and flow datasets; the multi-class dataset is built stratified and balanced. (Section IV-A; Section IV-B; Section V)",
        "Metrics": "Accuracy is the main metric because the datasets are balanced; ROC curves, AUC and true/false positive rates are reported for detection, and per-class accuracy, precision, recall and F1 score in a one-vs-all schema for multi-class. (Section IV-B; Section V; Table III)",
        "Reported results": "Binary detection: Raw Packets 77.6% test accuracy (AUC 0.84), Raw Flows 98.6% test accuracy (AUC 0.998), with all malware flows detected below 2.5% false alarms; the first packet-level evaluation detects more than 70% of malware packets below 3% false alarms. Multi-class per-class accuracy: Normal 0.878, Neris 0.635, Rbot 0.999, Virut 0.547. (Section IV-A; Section IV-B; Figs. 5, 7; Section V; Table III)",
        "Deployment limitations": "The authors state that raw-packet detection performance is not good enough to rely on in practice, that the packet-level representation shows potential over-fitting, and that raw packets are not discriminative enough for proper multi-class classification; testing multi-class with Raw Flows is left as ongoing work. (Section IV-A; Section IV-B; Section V)",
        "Leakage / shortcut risks": "Controlled capture conditions bias IP addresses, ports and some transport flags, which are not representative of in-the-wild traffic, so only payload bytes are analysed; the authors also suspect the shared spam activity of Neris and Virut is the root cause of confusion between them. (Section III-B; Section V; Table II)",
        "Version notes": "Values read from the arXiv preprint 2003.04079v2; the atlas cites the Springer chapter, so locators may differ. (corpus/deepmal.pdf)"
}, url['deepmal'], "Full text; field locators in each value")
    detail('deeppacket', {
        "Traffic unit definition": "Classification operates on individual network packets rather than whole flows. (Section 5.1.1)",
        "Input representation": "Each packet becomes a fixed-length byte vector containing its IP header and subsequent content, normalised by dividing byte values by 255. (Section 4.2, Pre-processing)",
        "Packets / bytes": "Each sample contains one packet represented by 1500 bytes, described as the IP header plus the first 1480 bytes of IP payload; shorter packets are zero-padded. (Section 4.2, Pre-processing)",
        "Preprocessing / anonymisation": "Preprocessing removes Ethernet headers, DNS packets and payload-free TCP control segments, pads UDP headers to match TCP header length, and masks IP addresses. Majority classes are randomly undersampled to reduce class imbalance. (Section 4.2; Section 4.2.1)",
        "Architecture": "The SAE uses fully connected layers of 400, 300, 200, 100 and 50 neurons; the CNN uses two convolutional layers followed by max pooling and fully connected layers of 200, 100 and 50 neurons. Both finish with task-specific softmax classifiers, and Tables 9 to 12 specify dropout of 0.05. (Section 4.3; Appendix A, Tables 9 to 12)",
        "Pretraining objective": "SAE layers are pretrained greedily to reconstruct their inputs using mean squared error and Adam. (Section 3.1; Section 5, SAE training)",
        "Pretraining datasets": "SAE layer-wise training uses the ISCX VPN-nonVPN training partition prepared for the classification tasks. (Section 4.1; Section 5, data partitioning and SAE training)",
        "Fine-tuning objective": "The complete SAE is fine-tuned with categorical cross-entropy; the CNN also uses categorical cross-entropy with Adam. (Section 5, training procedure)",
        "Training / evaluation datasets": "ISCX VPN-nonVPN is relabelled into 17 non-VPN application classes and 12 activity classes distinguishing VPN from non-VPN traffic. A separate experiment classifies underlying applications within Tor traffic. (Section 4.1; Section 4.2.1; Table 1; Section 6; Table 8)",
        "Split strategy": "Packet samples are randomly split into 64% training, 16% validation and 20% testing. (Section 5, experimental setup)",
        "Metrics": "Evaluation reports precision, recall and F1-score, including weighted averages; the application comparison also reports accuracy. (Section 5; Tables 3 to 5)",
        "Reported results": "For application identification, weighted F1-score is 0.98 for CNN and 0.95 for SAE; for traffic characterisation it is 0.93 and 0.92 respectively. On the Tor-only task, weighted F1-score falls to 0.36 for CNN and 0.30 for SAE. (Tables 3, 4 and 8, Wtd. average rows)",
        "Deployment limitations": "The authors identify real-world high-speed traffic handling as an unresolved implementation challenge and report poor classification of applications tunnelled through Tor. (Section 7, Future work; Section 6, Tor experiment)",
        "Leakage / shortcut risks": "The authors report that endpoint IP addresses uniquely identify applications in the dataset and mask them to prevent shortcut learning. They also state that CNN hyperparameters were selected to maximise weighted F1-score on the test set. (Section 5.1.1; Section 5, grid search procedure)"
}, url['deeppacket'], "Full text; field locators in each value")
    detail('distiller', {
        "Traffic unit definition": "Samples are bidirectional flows segmented using transport protocol, endpoint IP addresses and endpoint ports. (Section 4.1, TC Object)",
        "Input representation": "The payload modality uses normalised transport-payload bytes; the header modality uses payload length, TCP window size, inter-arrival time and packet direction. UDP window sizes are zero, and inputs are truncated or zero-padded to their configured lengths. (Section 3.3)",
        "Packets / bytes": "The evaluated input budgets are 784 transport-payload bytes and header information from the first 32 packets per biflow. (Section 4.2)",
        "Preprocessing / anonymisation": "Periodic BlueStacks broadcast traffic is removed. Inputs exclude PCAP metadata, data-link information and transport ports identified as potentially biased. (Sections 3.3, 4.1 and 4.2)",
        "Architecture": "The payload branch uses convolutional and pooling layers followed by a dense layer; the header branch uses a bidirectional GRU followed by a dense layer. Their features are concatenated into shared and task-specific dense layers with softmax outputs and dropout regularisation. (Section 3.3; Figure 2)",
        "Parameters": "DISTILLER has 0.97 million trainable parameters. (Section 5.1; Table 5)",
        "Pretraining objective": "Each modality branch is independently supervised using temporary softmax heads, minimising a weighted sum of categorical cross-entropies across the classification tasks. (Section 3.2; Equation (1))",
        "Pretraining datasets": "Modality pretraining uses the ISCX VPN-nonVPN training data employed in the paper's cross-validation evaluation. (Sections 3.2–3.3, 4.1 and 5)",
        "Fine-tuning objective": "After removing the temporary softmax heads, the combined model minimises weighted categorical cross-entropy across tasks. Convolutional and BiGRU feature-extraction layers are frozen while the remaining layers are fine-tuned. (Sections 3.2–3.3; Equation (2))",
        "Training / evaluation datasets": "The cleaned ISCX VPN-nonVPN dataset contains 11.6k biflows. Its tasks distinguish 2 encapsulation classes, 6 traffic types and 15 applications. (Sections 3.3 and 4.1; Table 3)",
        "Split strategy": "Stratified five-fold cross-validation is performed over biflow samples, stratifying by application labels; results report means and standard deviations across folds. (Section 5)",
        "Metrics": "The primary metrics are accuracy and macro F-measure; supplementary analyses use Top-K accuracy, per-class recall, expected calibration error, classified ratio and incoherence. Training efficiency is assessed using runtime per epoch and trainable parameter count. (Sections 5.1–5.4; Tables 4–6)",
        "Reported results": "On ISCX VPN-nonVPN, the reported F-measure gains over the overall-best baseline reach +8.45% for encapsulation, +7.58% for traffic type and +5.09% for application classification. (Section 6, summary of overall comparison)",
        "Hardware": "Experiments use an OpenStack virtual machine with 16 vCPUs and 32 GB RAM running Ubuntu 16.04. (Section 4.3)",
        "Measurement scope": "Efficiency measurements concern training runtime per epoch and trainable parameters, with classifiers run under the same load conditions. They do not constitute live traffic-processing throughput measurements. (Sections 4.3 and 5.1; Tables 4–5)",
        "Leakage / shortcut risks": "The authors identify PCAP metadata, data-link information and transport ports as sources of inflated performance and poor generalisation, and exclude them from model inputs. They also remove emulator broadcast traffic that dominates the uncleaned dataset. (Sections 3.3 and 4.1)"
}, url['distiller'], "Full text; field locators in each value")
    detail('dodont', {
        "Traffic unit definition": "The intrusion-detection experiment classifies packets using packet frequency within a 10-second sliding window. (Section 4.4, Experimental setup)",
        "Input representation": "The authors’ simple intrusion-detection baseline uses packet frequency as its sole feature. (Section 4.4, Experimental setup)",
        "Architecture": "The boxplot detector derives lower and upper thresholds from the clean calibration distribution using quartiles and the interquartile range; packets are malicious when their window frequency falls outside these thresholds. (Section 4.4, Experimental setup)",
        "Training / evaluation datasets": "The network-intrusion case study uses Mirsky et al.’s Mirai IoT capture, covering 119 minutes on a Wi-Fi network with three PCs and nine IoT devices. (Section 4.4, Dataset collection)",
        "Metrics": "The intrusion-detection experiment reports ROC AUC and true-positive rates at specified false-positive rates. (Section 4.4; Table 5)",
        "Reported results": "On the Mirai capture, the authors’ simple boxplot baseline achieves AUC 0.998 and TPR 0.996 at both FPR 0.001 and FPR 0.000. (Section 4.4; Table 5, Simple Baseline row)",
        "Evaluation setting": "The prevalence analysis reviews 30 security papers using two independent reviewers per paper and third-reviewer dispute resolution. Impact experiments examine Android malware classifiers, VulDeePecker, source-code authorship attribution and Kitsune, with the network case comparing Kitsune against a packet-frequency boxplot detector. (Section 3, Review process; Sections 4.1–4.4)",
        "Leakage / shortcut risks": "The authors report test, temporal and selective snooping, including preprocessing across training and test data; their Android experiment deliberately ignores temporal dependencies. They identify shortcuts involving app-market origins, vulnerability-dataset tokens, copied author templates and conspicuous packet-frequency changes in the Mirai capture. (Section 2.2, P3–P4; Sections 4.1–4.4; Appendix A, Table 8)",
        "Deployment limitations": "The authors explicitly caution that the boxplot experiment does not demonstrate detection of Mirai in the wild; the laboratory infection is overly conspicuous compared with the expected proportion of attack traffic in practice. (Section 4.4, Results)"
}, url['dodont'], "Full text; field locators in each value")
    detail('dpi', {
        "Traffic unit definition": "Application signatures are matched against individual TCP segments, with matches and traffic counters accumulated into bidirectional TCP connection records. (Sections 3 and 5.3)",
        "Input representation": "TCP payload signatures combine fixed-offset byte, word and string matches with variable-offset string searches. The targeted protocols are Gnutella, Kazaa, DirectConnect, BitTorrent and eDonkey. (Sections 4–5)",
        "Packets / bytes": "BitTorrent detection matches the first 20 payload bytes: a marker followed by the protocol string. More generally, the design targets signatures near the beginning of downloads rather than a uniform packet or byte budget. (Sections 3 and 4.4)",
        "Preprocessing / anonymisation": "TCP streams are not reassembled, and only the first fragment of a fragmented IP datagram is inspected. Cheap fixed-offset checks filter candidates before more expensive variable-offset matching. (Sections 3 and 5.3)",
        "Architecture": "Signature functions are integrated into Gigascope, whose configuration is translated into compiled C code for real-time monitoring. Fixed-offset checks precede variable-offset searches, and connection state records matches and traffic counts. (Sections 5.1–5.3)",
        "Training / evaluation datasets": "The Internet Access Trace covers a Tuesday and a Sunday in November 2003 at an access network to a major backbone. The VPN Trace covers 6 days, 1.8 Terabytes and 2.8 billion packets on an employee VPN link. (Section 6.1)",
        "Metrics": "False positives measure non-application traffic identified as application traffic, and false negatives measure application traffic missed. Further metrics include one-direction detection coverage, packets examined before a match, and signature-search throughput. (Sections 6.2–6.3 and 7.1–7.2; Tables 1–3)",
        "Reported results": "On Internet Access Trace connections with payload, byte-based FN ratios are 1.03% for Gnutella, 4.70% for Kazaa, 0% for DirectConnect, 9.89% for BitTorrent and 1.60% for eDonkey. The VPN experiment reports zero false positives conditional on correct manual verification. (Section 7.1.1; Table 1, Connections with payload FN(%) column)",
        "Hardware": "Micro-benchmarks use a Dell Power Edge 2650 with two 2.8GHz processors running FreeBSD 4.7. (Section 6.3, Micro-benchmarking)",
        "Throughput": "AST regex achieves 77.60%, 58.7% and 8.7% of the warm-cache loading throughput for Kazaa, Gnutella and DirectConnect signatures, respectively. These are offline trace-processing measurements relative to loading the same data without searching. (Section 7.2; Table 3, AST regex column)",
        "Measurement scope": "The scalability micro-benchmarks time signature searches over cached packet traces, with no-search file loading as the reference. Separate experiments apply the classifier to VPN traffic in real time. (Sections 6.3, 7.1.1 and 7.2)",
        "Evaluation setting": "VPN detections are manually inspected to assess false positives; false negatives are estimated by treating traffic on default application ports as application traffic. Robustness is tested by restricting signature visibility to either direction of otherwise bidirectionally observed connections. (Sections 7.1.1–7.1.3)",
        "Deployment limitations": "Packet-level matching can miss signatures spanning packet boundaries, and connection timeouts can create unrecognisable split connections. The authors expect increased encryption to undermine application-signature classification. (Section 6.2; Section 8)"
}, url['dpi'], "Full text; field locators in each value")
    detail('early', {
        "Traffic unit definition": "A TCP connection is classified from its initial data packets in both directions; evaluation requires at least four data packets. (Sections 2.2, 4 and 5.4.3)",
        "Input representation": "Connections are represented by ordered, signed payload sizes, positive for client packets and negative for server packets, using either a Euclidean vector or an HMM sequence. Cluster & Port labelling additionally uses the server port. (Sections 5.2 and 6.2)",
        "Packets / bytes": "The selected classifiers use the first four data packets of each TCP connection. (Section 5.4.3)",
        "Preprocessing / anonymisation": "Non-TCP packets and connections beginning before capture are removed. TCP control packets without application data are discarded. (Section 2.2)",
        "Architecture": "Offline training uses K-Means or Gaussian mixtures on Euclidean representations, or spectral clustering on HMM representations, followed by online cluster assignment and application labelling. The selected configurations use 40 K-Means, 45 GMM and 30 HMM clusters. (Sections 4–6, especially Section 5.4.3)",
        "Training / evaluation datasets": "Training draws labelled connections from Paris6-1, Paris6-2 and Paris6-3; evaluation also uses Enterprise, M2C College, M2C ADSL, Crawdad and UMass traces. Separate BitTorrent, IMAP, Gnutella, IRC, LDAP, MSN and Mysql traces test applications absent from training. (Sections 2.1–2.4, 5.1 and 7.3; Table 1)",
        "Split strategy": "Training randomly selects 500 connections from each eligible application in the Paris 6 traces; classification is evaluated on the named test traces. (Sections 5.1 and 7.1; Table 2)",
        "Metrics": "NMI measures clustering quality; assignment accuracy measures whether the assigned cluster contains the true application, while labelling accuracy measures correct application labels among assigned connections. Per-application true positives, false positives, false negatives, unknown and masquerade proportions are also reported. (Sections 5.4.1 and 7.1–7.3)",
        "Reported results": "With GMM Proba and Cluster & Port labelling, Table 3 reports 98.5% accuracy on Paris6-1 and 99.1% on Enterprise. With GMM thresholds, Table 5 reports 66.8% of BitTorrent connections labelled unknown, but 0.0% of Gnutella connections labelled unknown. (Table 3, Cluster&Port rows and GMM Proba column; Table 5, GMM Thresh Unknown column, Bittorrent and Gnutella rows)",
        "Memory": "The proposed classifier stores initial packet sizes and the TCP port, requiring a few bytes per connection. (Section 7.4)",
        "Measurement scope": "Efficiency is discussed through operation counts and storage requirements; implementation and evaluation of an online classifier are left to future work. (Section 7.4)",
        "Deployment limitations": "The classifier requires the initial data packets in their correct order, and packet sampling or reordering can impair performance. Attackers can evade the method by padding payloads to alter packet sizes. (Section 8)",
        "Version notes": "For Paris6-1 GMM labelling, Table 3 gives 93.5% with Dominant and 98.5% with Cluster & Port, whereas Table 4 gives overall values of 93.7% and 98.7%, respectively. (Table 3, P6-1 rows and GMM Proba column; Table 4, GMM without Threshold Overall row)"
}, url['early'], "Full text; field locators in each value")
    detail('evs2vec', {
        "Traffic unit definition": "Byte Rate Sequence (BRS): bytes transferred per second, binned at 1-second intervals over the whole sniffed playback traffic, of indefinite length; no per-flow (5-tuple) separation is applied, so the unit is the aggregate traffic during playback rather than a flow. (Section II-B; Section III-A (Algorithm 1))",
        "Input representation": "A variable-length BRS of per-second byte counts is fed element-by-element into the RNN; padding and masking handle differing lengths within each training batch, and training consumes random pairs of BRSs. (Section III-B1; Section III-C)",
        "Packets / bytes": "No fixed packet or byte budget per sample: BRS sums the payload lengths of all TCP packets captured per second (the protocol field filters for TCP), so sample length varies with playback duration. (Section III-A; Algorithm 1)",
        "Preprocessing / anonymisation": "No IP/port masking, 5-tuple flow splitting, TCP reassembly or packet dividing and merging is needed; BRS can be generated directly during sniffing without saving the original traffic data. (Section II-B; Section III-A)",
        "Architecture": "3-layer RNN (32 cells per layer; GRU in the experiments, LSTM possible) with scaled dot-product self-attention over the RNN outputs and global average pooling, then FC(64, 32, ReLU) and FC(32, 8) fully connected layers with two batch-normalisation layers, yielding an 8-dimensional embedding; trained as weight-sharing siamese twins. (Section III-B; Fig. 4)",
        "Fine-tuning objective": "No pretraining; the model is trained end-to-end as a siamese network on random BRS pairs labelled same or different video title, minimising a contrastive loss on the L2-norm embedding distance with margin 1. (Section III-C; Section V-A)",
        "Training / evaluation datasets": "The public Dubin et al. YouTube dataset [3]: 10,000 encrypted YouTube streams of 100 titles (100 streams per title), collected via real-world Internet connections over different network conditions using Selenium with ChromeDriver in Chrome. It supports training plus thresholding on 100,000 test-set stream pairs, a 10-title fingerprinting example, and classification and clustering over the 50 test titles. (Section V-B; Sections V-C to V-F)",
        "Split strategy": "Stream-level 1:1 train/test split, disjoint by title: 50 titles form the training set and the remaining 50 titles the test set. Training pairs are sampled 1:1 same-title versus different-title, classifiers are trained on half the embedding results and tested on the other half, and the saved model is the checkpoint performing best on the test set. (Sections V-A, V-B and V-E)",
        "Metrics": "ROC threshold accuracy (threshold chosen by Youden's index from TPR/FPR), classification accuracy, per-title F1 scores tallied above 0.80/0.90/0.95, and clustering accuracy and F1; no macro, weighted or micro averaging is stated. (Sections V-C to V-F; Tables I and II)",
        "Reported results": "On the Dubin YouTube dataset, EVS2vec reaches 96.707% threshold-discrimination accuracy (96.71% in the abstract) at ROC threshold 0.30835, classification accuracy up to 0.9739 with Random Forest on its 8-dimensional embeddings (XGBoost 0.9554, SVM 0.9269) and best clustering accuracy 0.7331 with agglomerative clustering, with roughly 20-30% of titles at F1 above 0.95. Under Rayleigh noise with mean below 100MB/s the attention-based models keep about 95% threshold accuracy, while variants without self-attention dip for noise means of 10B/s to 1KB/s. (Abstract; Sections V-C, V-E, V-F and V-G; Tables I and II; Fig. 8)",
        "Hardware": "Intel Core i9-10900K CPU at 3.70GHz, NVIDIA GeForce RTX 3090 GPU and 128GB of RAM; implemented in TensorFlow 2.9.0. (Section V-A)",
        "Deployment limitations": "Training uses only rough same-title similarity, so semantic analysis of the embeddings is limited; the training data comes from one website (YouTube), restricting cross-platform analysis; UDP-based scenarios such as online video calls or conferences remain to be studied. (Section VI)"
}, url['evs2vec'], "Full text; field locators in each value")
    detail('flowprint', {
        "Traffic unit definition": "FlowPrint processes TCP/UDP flows separately per device in 300-second batches, using 30-second activity windows to correlate destination clusters. (Sections IV-A–IV-D; Section V-A; Table III, final row)",
        "Input representation": "Destination IP/port tuples and TLS certificates identify destination clusters, while packet timestamps establish temporal correlations. Packet sizes and directions support browser isolation, and fingerprints are sets of destinations forming maximal cliques. (Sections IV-A–IV-E)",
        "Preprocessing / anonymisation": "Traffic is handled separately per device without using source IP as a fingerprint feature; domain names are excluded because DNS information may be unavailable. Detected browser connections are isolated before destination correlation and fingerprint construction. (Section II-D, Device features and Destination features; Section IV-C)",
        "Architecture": "The pipeline combines destination clustering, a random-forest browser detector, normalised temporal cross-correlation, maximal-clique fingerprint construction and Jaccard matching. The selected correlation and fingerprint-similarity thresholds are 0.1 and 0.9 respectively. (Sections IV-B–IV-F; Section V-A; Table III, final row)",
        "Training / evaluation datasets": "Evaluation uses ReCon with 512 Android apps, ReCon extended with five apps, Cross Platform with 215 Android and 196 iOS apps, and Andrubis with 1.03 million Android apps. The separately collected Browser dataset covers four browsers. (Section II-A; Table I)",
        "Split strategy": "Each app’s traffic is split 50:50 into non-overlapping training and testing sets; app experiments use randomly selected apps and cross-validation. Parameter selection uses held-out Andrubis validation data excluded from the remaining evaluation, while browser-detector data use an 80:20 training/testing split. (Section V, Experimental setup; Sections V-A and V-D)",
        "Metrics": "App recognition reports precision, recall, F1-score and accuracy, described as micro-averaged over individual apps; unseen-app detection reports the same metrics with unknown apps as positives. Fingerprint confidence is measured using entropy-based homogeneity. (Sections V-B–V-D; Tables IV, V and VII; Equation 6)",
        "Hardware": "Execution-time experiments run on a single core of an HP Elitebook laptop with an Intel Core i5-5200U CPU at 2.20 GHz. (Section V-G)",
        "Throughput": "The fingerprint-generation benchmark processes roughly 400,000 flows within a five-minute batch interval. (Section V-G; Figure 10)",
        "Latency": "Fingerprint matching against a database containing one million fingerprints takes 73 seconds in the reported benchmark. (Section V-G; Figure 11)",
        "Measurement scope": "Execution-time experiments separately benchmark fingerprint generation, including clustering, and matching 1,000 generated fingerprints against varying database sizes, averaging over 10 runs. Processing complexity is expressed in flows rather than communicated bytes. (Section V-G; Figures 10 and 11)",
        "Deployment limitations": "Low-traffic apps communicating only with widely shared services can be difficult to distinguish, and simultaneously active apps can produce composite fingerprints. Multiple fingerprints may represent one unseen app, destination changes degrade recognition over time, and a system-wide VPN or proxy obscures identification of individual apps. (Section III; Section V-E; Section VI, Low-traffic apps, Simultaneously active apps, Fingerprint coverage and Potential for evasion)",
        "Leakage / shortcut risks": "The authors acknowledge that app-version experiments may be biased because traffic from versions released over an extended period was collected within a much shorter capture period. They separately simulate destination changes and perform a later real-world recapture to assess temporal degradation. (Section V-E, App updates and Longitudinal analysis)"
}, url['flowprint'], "Full text; field locators in each value")
    detail('flowrest', {
        "Traffic unit definition": "Traffic is classified at the flow level, identified by a 5-tuple hash, with early-flow inference performed upon the third packet of each flow. (Section III-C)",
        "Input representation": "Stateless packet features (TCP/UDP ports, packet length, TCP flags) combined with stateful flow features (packet length statistics, inter-arrival time statistics, flow duration, and TCP flag counts). (Section III-E)",
        "Packets / bytes": "Inference is executed on the third packet of a flow (n = 3) using statistics accumulated from the preceding packets. (Section III-C)",
        "Preprocessing / anonymisation": "IP and MAC addresses are deliberately excluded to avoid shortcut learning; features exceeding hardware range match bit limits undergo binary bit-shifting and truncation. (Section III-E)",
        "Architecture": "Random Forest implemented across PISA Match-Action Units (MAUs), where each feature is assigned to one MAU and the final stage evaluates codeword paths using TCAM matches. Hyperparameters span from 2 trees of depth 3 to 3 trees of depth 11. (Section III-E)",
        "Training / evaluation datasets": "UNSW-IoT evaluated on 16 and 26 classes, UNIBS-2009 evaluated on 8 application classes, and CICIDS2017 (Friday traffic) evaluated on binary benign versus attack classification. (Section IV-B)",
        "Split strategy": "UNSW-IoT used 15 days of data for training and 1 day for testing; UNIBS-2009 used one day for training and one day for testing; CICIDS2017 used a 75:25 train-test split. (Section IV-B)",
        "Metrics": "Precision, recall, and F1 score. (Section IV-C)",
        "Reported results": "F1 starts at 0.99 for the binary task and stays at 0.86 with 26 classes; accuracy up to 39% higher than previous approaches to implementing RF models in real switches. (Abstract; Section IV-D)",
        "Hardware": "Edgecore Wedge100BF-QS programmable switches equipped with an Intel Tofino BFN-T10-032Q ASIC and 32 100GbE QSFP28 ports running Open Network Linux and SDE 9.7.0, paired with Intel 8-core Xeon 2 GHz servers with 48 GB RAM. (Section IV-A)",
        "Throughput": "Operates at line rate across a 100 Gbps testbed replaying packet traces using Tcpreplay. (Section IV-A)",
        "Memory": "Consumes 15% to 29% of average switch resources relative to the baseline switch.p4 program, using additional SRAM and VLIW for flow tracking while adding no extra TCAM or PHV overhead over packet-level RF. (Section IV-D)",
        "Measurement scope": "Resource usage covers switch pipeline allocation (SRAM, VLIW, TCAM, PHV) compared against the baseline L2/L3 switch.p4 configuration. (Section IV-D)",
        "Deployment limitations": "Hash collisions occur in the flow management table due to limited register sizes; the closed-loop controller update introduces a reconfiguration delay of seconds; and the maximum ternary match width restricts the number of leaf nodes per tree. (Section III-B; Section III-C; Section III-E)",
        "Leakage / shortcut risks": "Including IP or MAC addresses allows models to memorise specific hosts in constrained datasets, artificially inflating accuracy and causing models to fail on unseen hosts in deployment. (Section III-E)"
}, url['flowrest'], "Full text; field locators in each value")
    detail('fsnet', {
        "Traffic unit definition": "flow sequences as input units. (Section III-A)",
        "Input representation": "packet length sequences with embedding. (Section V-B.2)",
        "Preprocessing / anonymisation": "packet recombination and flow reduction. (Section V-A)",
        "Architecture": "7-layer end-to-end hierarchical model with embedding, stacked bi-GRU encoder/decoder, reconstruction, dense and classification layers. (Section IV)",
        "Training / evaluation datasets": "real-world campus network dataset from [11] with 956+ thousand encrypted flows across 18 applications, collected over 7 days. (Section V-A)",
        "Split strategy": "5-fold cross validation at flow level. (Section V-A)",
        "Metrics": "TPR, FPR, FTF, T P RAV E, F P RAV E. (Section V-B.3)",
        "Reported results": "99.14% TPR, 0.05% FPR, 0.9906 FTF; T P RAV E 0.9914, F P RAV E 0.0005, FTF 0.9906 on 18-application dataset. (Abstract; Table III)",
        "Evaluation setting": "comparison against FoSM, SOCRT, SOB, FoLM, SOB-L, MaMPF on same dataset and metrics. (Section V-B.1)"
}, url['fsnet'], "Full text; field locators in each value")
    detail('manyfew', {
        "Traffic unit definition": "Biflow defined by the 5-tuple (source and destination IP addresses, ports, and Layer 4 protocol), focusing on the first 10 or 20 packets. (Section V-A)",
        "Input representation": "Packet time series capturing 4 features (packet size, direction, inter-arrival time, and TCP window size) for MIRAGE19, and 2 features (packet size and direction) for AppClassNet. (Section V-A)",
        "Packets / bytes": "First 10 packets per biflow for MIRAGE19 and first 20 packets per biflow for AppClassNet, with UDP window size padded with zeros. (Section V-A)",
        "Preprocessing / anonymisation": "AppClassNet removed IP addresses, exact timing, header fields, and payloads, whilst anonymising application labels and raw time-series values; MIRAGE19 padded UDP TCP window-size features with zero. (Section V-A)",
        "Architecture": "Two 2D CNN backbones: CNN-2 consists of two 2D convolutional blocks with 32 and 64 filters followed by batch normalisation, ReLU, and a 200-unit fully connected layer; CNN-4 includes four convolutional blocks and a 500-unit fully connected layer. (Section V-B)",
        "Parameters": "CNN-2 trunk has 529k parameters and CNN-4 trunk has 1.3M parameters. (Section V-B)",
        "Pretraining objective": "Cross-entropy or cosine-distance loss for transfer learning baselines, and InfoNCE loss using four time-series augmentations for unsupervised (SimCLR) and supervised (SupCon) contrastive learning. (Section II-D; Section V-B)",
        "Pretraining datasets": "Disjoint source training partitions: MIRAGE19 source task with 24 classes (82k samples) and AppClassNet source task with 320 classes (9.8M samples). (Section V-A; Table III)",
        "Fine-tuning objective": "Target task evaluation fine-tunes classifier heads using episodic training with S shots and 15 queries per episode, or full-dataset monolithic fine-tuning with fixed feature extractors. (Section V-B; Section V-D)",
        "Training / evaluation datasets": "MIRAGE19 (40 Android application classes total, split into 24 train, 8 validation, 8 test) and AppClassNet (500 application classes total, split into 320 train, 80 validation, 100 test). (Section V-A; Table III)",
        "Split strategy": "Class-disjoint partitioning based on class popularity: Dtrain receives the most popular classes, while Dval and Dtest receive disjoint sets of less popular classes; monolithic models partition Dtrain into 9:1 train/validation splits. (Section V-A; Section V-D)",
        "Metrics": "Balanced accuracy, computed as the weighted average of per-class accuracy weighted by the inverse of class popularity. (Section V-D)",
        "Reported results": "In 4-way 200-shot target tasks, SupCon(ClassEmb) achieves 91.87 ± 0.37% on MIRAGE19 and 95.94 ± 0.44% on AppClassNet, while Baseline(NN) achieves 92.84 ± 0.24% on MIRAGE19 and 93.77 ± 0.29% on AppClassNet. (Section VI-B; Table V)",
        "Hardware": "Multiple Linux servers equipped with multiple Nvidia V100 GPUs. (Section V-D)",
        "Memory": "Pickle serialization model memory is 2.2MB for CNN-2 and 5.4MB for CNN-4, compared to 930MB and 416GB for unbounded Random Forest on MIRAGE19 and AppClassNet respectively. (Section VI-A)",
        "Deployment limitations": "DL deployment is constrained by GPU/TPU accelerator availability and optimisation demands, high computational costs for contrastive learning augmentations (around 1 day per source model), and the need for nearest-neighbour classifiers to carry training anchor samples. (Section VI-A; Section VI-B)",
        "Evaluation setting": "Comparative evaluation of 16 methods across monolithic DL, transfer learning (8 variants), meta-learning (MAML, ProtoNet, RelationNet), and contrastive learning (SimCLR, SupCon with and without class embeddings) alongside Random Forest baselines. (Section I; Section V-B)"
}, url['manyfew'], "Full text; field locators in each value")
    detail('mimetic', {
        "Traffic unit definition": "biflow (stream of packets sharing the 5-tuple, irrespective of direction). (Section 3.1; Section 3.3)",
        "Input representation": "two modalities: first Nb bytes of payload (normalised to [0,1]) and first Np packets with protocol fields (transport-layer payload bytes, TCP window size, inter-arrival time, direction). (Section 3.3)",
        "Packets / bytes": "576 bytes of payload, 12 packets for protocol fields. (Section 3.3; Section 5.1)",
        "Preprocessing / anonymisation": "datasets anonymised and cleaned from background traffic; port information excluded to prevent bias. (Section 4.1; Section 3.3)",
        "Architecture": "Multimodal: payload branch (two 1D-CNN layers with 16 and 32 filters, kernel 25, stride 1, ReLU; each followed by 1D max-pooling with stride 1, extent 3; then dense layer with 256 nodes) plus protocol fields branch (bidirectional GRU with 64 nodes, return-sequences; then dense layer with 256 nodes); merge via concatenation; shared dense layer with 128 nodes; softmax. (Section 3.3; Fig. 2)",
        "Parameters": "approximately 3.6 times fewer trainable parameters than 1D-CNN, 4.1 times fewer than TLF. (Section 5.3; Fig. 3(b))",
        "Pretraining objective": "weighted categorical cross-entropy for each modality independently. (Section 3.2; Eq. (1))",
        "Pretraining datasets": "same mobile traffic training sets (FB/FBM, Android, iOS). (Section 3.2)",
        "Fine-tuning objective": "weighted categorical cross-entropy for the full multimodal architecture. (Section 3.2; Eq. (2))",
        "Training / evaluation datasets": "FB/FBM (approximately 31k biflows from Facebook and Facebook Messenger, 91 percent encrypted), Android (55.5k labeled biflows from 49 apps, 47 percent encrypted), iOS (37.2k labeled biflows from 45 apps, 60 percent encrypted). (Section 4.1)",
        "Split strategy": "stratified ten-fold cross-validation. (Section 4.2)",
        "Metrics": "accuracy, precision, recall, macro-averaged F-measure, Top-K accuracy, confusion matrices, classified ratio. (Section 4.2)",
        "Reported results": "FB/FBM: 79.98 percent accuracy, 79.63 percent F-measure; Android: 89.49 percent accuracy, 81.51 percent F-measure, 95.82 percent Top-5 accuracy; iOS: 89.14 percent accuracy, 82.99 percent F-measure, 96.74 percent Top-5 accuracy; up to plus 8.58 percent improvement. (Table 3; Table 4; Section 5.2)",
        "Hardware": "8 × Intel Core i7-4710MQ CPU at 2.50GHz, Ubuntu 16.04 64-bit. (Section 5.3)",
        "Measurement scope": "training phase runtime and trainable parameters; covers training complexity only. (Section 5.3)",
        "Deployment limitations": "fixed-length inputs require truncation or zero-padding; biflow-level classification only. (Section 3.3)",
        "Evaluation setting": "Comparison against single-modality DL (1D-CNN with L7-784, LSTM+2D-CNN with MAT-20), shallow MLP-1, flow-based RF, and fusion techniques (MV, SOA, TLF). (Section 5.1)",
        "Leakage / shortcut risks": "port information excluded to prevent biased and inflated performance. (Section 3.3)"
}, url['mimetic'], "Full text; field locators in each value")
    detail('miniflowpic', {
        "Traffic unit definition": "Samples are session windows: QUIC uses the first 15 seconds of each session, while ISCX yields multiple non-overlapping windows of the same duration. (Sections 2.2, 3.1.1 and 3.1.2)",
        "Input representation": "Mini-FlowPics are packet-count histograms over packet-size ranges and time slots, normally represented as 32x32 images. (Sections 2.1 and 2.2)",
        "Packets / bytes": "QUIC and ISCX retain sessions containing at least 100 packets; packets larger than 1500 bytes are discarded when constructing FlowPics. (Sections 2.1, 3.1.1 and 3.1.2)",
        "Preprocessing / anonymisation": "QUIC preprocessing removes non-QUIC sessions and sessions with fewer than 100 packets; ISCX is also filtered by the minimum session packet count. (Sections 3.1.1 and 3.1.2)",
        "Architecture": "A LeNet-5-based CNN provides the backbone; the representation extractor retains its first five layers and replaces the final two with linear layers producing a 120-dimensional representation and a 30-dimensional projection. (Appendices A.1 and A.2)",
        "Pretraining objective": "Unsupervised SimCLR contrastive learning brings augmented views of the same sample together and separates other samples, using cosine similarity with a temperature parameter. (Section 2.4; Appendix A.2)",
        "Pretraining datasets": "The QUIC and ISCX datasets used in supervised experiments are reused without labels, with 100 samples per class for representation learning. (Section 3.3)",
        "Fine-tuning objective": "The encoder is frozen and a linear classifier is trained on a few labelled examples using categorical cross-entropy. (Section 3.3; Appendix A.3)",
        "Training / evaluation datasets": "UC-Davis QUIC covers Google Docs, Google Drive, Google Music, Youtube and Google Search, with script-triggered and human-triggered evaluation sets. The ISCX-VPN and ISCX-Tor combination supplies 10 non-VPN VoIP and video application classes. (Sections 3.1.1 and 3.1.2)",
        "Split strategy": "QUIC trains on script-triggered flows and tests on separately selected script-triggered and human-triggered flows. ISCX sessions are separated into disjoint training and test groups before sampling FlowPics. (Sections 3.1.1 and 3.1.2)",
        "Metrics": "Classification accuracy is reported; few-shot plots show mean accuracy over 10 experiments with randomly selected training samples and standard-deviation whiskers. (Section 3.3; Figures 3–5)",
        "Reported results": "Few-shot QUIC script classification achieves 93.4% accuracy with 3 labelled samples per class and 94.5% with 10. Supervised RTT augmentation with mini-FlowPic 32 achieves 99.4% on QUIC script, 96.4% on QUIC human and 91.0% on ISCX Video and VoIP. (Section 3.3; Tables 1–3, Change RTT rows)"
}, url['miniflowpic'], "Full text; field locators in each value")
    detail('nprint', {
        "Traffic unit definition": "nPrint represents individual packets; multi-packet samples are constructed by concatenating packet representations. Case studies classify device probe responses, operating-system packet groups, DTLS handshakes, flows and traffic traces. (Section 2.2.3; Sections 5.1 to 5.4)",
        "Input representation": "The representation aligns raw packet bits by protocol, zero-pads existing headers to their maximum size and fills absent headers with a sentinel. Payload inclusion is configurable. (Section 2.2.3; Figure 3)",
        "Packets / bytes": "Active device fingerprints contain 21 packet slots; passive OS experiments use groups of 1, 10 or 100 packets, and DTLS samples are padded to 43 packets. Figure 3 allocates 60 bytes each for IPv4 and TCP headers and 8 bytes each for UDP and ICMP, with configurable payload bytes. (Figure 3; Section 5.1; Section 5.2; Section 5.3; Table 1)",
        "Preprocessing / anonymisation": "Passive OS experiments remove IP addresses, IP identification, TCP ports, and TCP sequence and acknowledgement numbers; netML experiments remove IP addresses. Active fingerprints are ordered by probe name, and missing responses receive sentinel padding. (Section 5.1, Packet Transformation and Data Representation; Section 5.2; Section 5.4.1)",
        "Architecture": "nPrintML combines nPrint with AutoGluon-Tabular for feature selection, model search and hyperparameter optimisation; the highest-performing models are ensembles. Base learners include random forests, ExtraTrees, KNeighbours, LightGBM, CatBoost and neural networks. (Section 4.1; Table 8)",
        "Fine-tuning objective": "Supervised model selection tunes hyperparameters and ensemble weights to maximise validation macro F1-score. (Section 4.1)",
        "Training / evaluation datasets": "Case studies use the Network Device Dataset augmented with IoT devices, CICIDS2017, DTLS handshakes, netML IoT, netML Non-VPN, netML CICIDS2017, Cross Platform mobile traces and Streaming Video Providers. Tasks cover device and OS identification, application identification, malware and intrusion detection, mobile country of origin and streaming provider identification. (Table 1; Sections 5.1 to 5.4)",
        "Split strategy": "Every dataset is split into 75% training and 25% testing, with 10-fold bagging during training. An additional OS generalisation experiment trains on one Ubuntu and one Windows host and tests on the remaining hosts. (Section 4.1; Section 5.2, nPrintML differentiates OSes, not simply devices)",
        "Metrics": "Reported metrics include balanced accuracy, macro F1-score and macro one-versus-rest ROC AUC; active fingerprinting also reports per-class average precision. (Section 4.2, Metrics; Section 5.1; Table 3)",
        "Hardware": "Offline encoding benchmarks use a four-core Intel Core i7-8559U at 2.7 GHz with 32 GB RAM. The operational-link experiment uses two Intel Xeon 6154 CPUs, each with 18 cores at 3 GHz, and 376 GB RAM. (Section 3, nPrint transforms over 1 million packets per minute and Proof of Concept)",
        "Throughput": "Single-threaded encoding averages approximately 1.5 million packets per minute on stored datasets. On live traffic, 16 queues and 16 nPrint processes handle roughly 8 Gbps with near-zero loss. (Section 3, offline performance benchmark and operational-link proof of concept)",
        "Latency": "For active device fingerprinting, Table 5 reports total inference times of 267 seconds and 3 seconds for nPrint ensembles scoring 95.4 and 95.2 F1 respectively. For DTLS classification, Table 8 reports 0.45 seconds total test-set inference time for the weighted ensemble. (Table 5, nPrint rows; Table 8, Weighted Ensemble row; Section 5.3)",
        "Memory": "Valgrind profiling gives a constant encoder footprint of approximately 295 KB for IPv4 and TCP output, or 310 KB when IPv4, UDP, ICMP, TCP and 10 payload bytes are included. (Section 3, nPrint has a constant memory footprint)",
        "Measurement scope": "Encoding throughput and memory measurements concern the nPrint transformation tool, including its CSV output, while model inference times are reported separately for test datasets. The live-link experiment measures packet processing by parallel nPrint processes. (Section 3; Section 5.3; Table 8)",
        "Deployment limitations": "The authors identify CSV output and libpcap processing as implementation bottlenecks. Capturing temporal relationships across flows and applying nPrintML to longer traffic sequences remain unexplored. (Section 3; Section 1, discussion following Table 1)",
        "Leakage / shortcut risks": "OS experiments remove direct device identifiers, test on unseen hosts and restrict packets to initial TTL values to investigate device and location memorisation. In active fingerprinting, the authors find that distinctive open ports identify IoT device classes. (Section 5.1, feature-importance discussion; Section 5.2, generalisation and initial-TTL experiments)",
        "Version notes": "The DTLS narrative reports 99.8% F1-score for the weighted ensemble, whereas Table 8 lists 99.9. The OS preprocessing description removes IP identification, but the subsequent feature-importance discussion still identifies IPID as useful. (Section 5.3, nPrintML can automatically detect features in a noisy environment; Table 8; Section 5.2)"
}, url['nprint'], "Full text; field locators in each value")
    detail('refinery', {
        "Traffic unit definition": "Traffic is tracked as flows identified by the IP and port 4-tuple, aggregated into time bins such as ten-second intervals for video quality inference, with an idle flow timeout of 10 minutes in the cache. (Section 3.1.2; Section 5.1.1)",
        "Input representation": "Input representations include network-layer packet counters, transport-layer TCP metrics, application-layer video segment metrics, or raw packet bytes converted to gray-scale PNG images or byte sequences. (Section 5.1.1; Section 5.2)",
        "Packets / bytes": "Input byte sizes evaluated for malware detection CNNs are square grids of 6x6 (36 bytes), 10x10 (100 bytes), 16x16 (256 bytes), 20x20 (400 bytes), and 28x28 (784 bytes), extracted from packet header fields. (Section 5.2.2; Section 5.2.3)",
        "Preprocessing / anonymisation": "Network traffic was anonymised and sanitised to remove personal information prior to processing, and service mapping was performed using DNS lookups and IP prefix matching. (Section 3.1.1; Section 4, footnote 1)",
        "Architecture": "Random forest regressors and multi-class classifiers are employed for video quality metrics, while a convolutional neural network is used for malware detection. (Section 5.1.3; Section 5.2.3)",
        "Training / evaluation datasets": "Evaluation uses a video streaming dataset containing over 13,000 sessions across four services (Netflix, YouTube, Amazon Prime Video, and Twitch), the CICIDS2017 dataset containing approximately 171,000 flows, and live traffic on a 10 Gbps interconnect link. (Section 4; Section 5.1.3; Section 5.2.2)",
        "Split strategy": "Malware detection cost-performance analysis is conducted on a hold-out test set of 19,000 flows from CICIDS2017. (Section 5.2.3)",
        "Metrics": "Evaluated metrics include Mean Absolute Error in milliseconds for startup delay, classification accuracy for video resolution, and F1 score for malware detection. (Section 5.1.3; Section 5.2.3; Figure 6; Figure 9a)",
        "Hardware": "A commodity server fitted with 16 Intel Xeon CPUs running at 2.4 GHz, 64 GB RAM, running Ubuntu 18.04, and connected to a 10 GbE network interface. (Section 4)",
        "Latency": "Cache insert time for a newly seen flow takes roughly 6,000 nanoseconds, compared to 200 nanoseconds for updating an existing flow entry. (Section 4)",
        "Memory": "The flow cache implementation supports creating a maximum of roughly 150,000 new flows per second. (Section 4)",
        "Deployment limitations": "The pipeline relies on unencrypted DNS or SNI which is threatened by encrypted DNS protocols, does not support cross-flow or event-based features, and encounters packet drops during sudden bursts exceeding 100,000 new flows due to cache locking overhead. (Section 3.1.1; Section 3.2; Section 4)"
}, url['refinery'], "Full text; field locators in each value")
    detail('survey', {
        "Traffic unit definition": "Unidirectional flows sharing a 5-tuple (source and destination IP addresses, source and destination ports, and protocol number), bidirectional flow pairs, and full-flows captured over their entire lifetime. (Section III-B)",
        "Evaluation setting": "The survey reviews and qualitatively assesses 18 works from 2004 to early 2007 spanning unsupervised, supervised, and hybrid ML techniques against four operational deployment requirements: real-time classification, feature computation overhead, continuous classification, and directional neutrality. (Abstract; Section IV-E5; Table IV)",
        "Deployment limitations": "Practical operational deployment requires classifiers to make decisions using as few packets as possible, perform continuous classification throughout flow lifetimes, handle flow asymmetry without directional knowledge, and maintain robustness against loss and jitter. (Section III-C; Section III-C1)",
        "Leakage / shortcut risks": "Evaluating classifiers using cross-validation on datasets collected at a single point in time and at the same network monitoring location risks over-estimating classification performance. (Section III-B1)"
}, url['survey'], "Full text; field locators in each value")
    detail('tfegnn', {
        "Traffic unit definition": "Traffic segments (TS) as samples with max 50 packets per sample. (Section 2.1; Section 4.1.3)",
        "Input representation": "Byte-level traffic graphs constructed via PMI between bytes. (Section 3.1)",
        "Packets / bytes": "Max 50 packets per sample; max 150 payload bytes and 40 header bytes. (Section 4.1.3)",
        "Preprocessing / anonymisation": "Remove bad/retransmission packets, packets without payload, Ethernet header, IP addresses and port numbers. (Section 4.1.2)",
        "Architecture": "Dual embedding (header/payload), GraphSAGE encoder (≤4 layers), cross-gated fusion, bidirectional 2-layer LSTM downstream. (Section 3.2; Section 3.3; Section 3.4)",
        "Parameters": "44M parameters; PMI window size 5; GraphSAGE ≤4 layers; embedding dimension 50. (Section 4.1.3; Table 4)",
        "Fine-tuning objective": "Cross-entropy loss for classification. (Section 3.4)",
        "Training / evaluation datasets": "ISCX VPN-nonVPN (6 classes), ISCX Tor-nonTor (8 classes), WWT (WeChat 12, WhatsApp 9, Telegram 6). (Section 4.1.1)",
        "Split strategy": "Stratified 9:1 train-test split. (Section 4.1.1)",
        "Metrics": "Overall Accuracy, Precision, Recall, Macro F1-score. (Section 4.1.3)",
        "Reported results": "F1: WeChat 0.9946, WhatsApp 0.9961, Telegram 0.9649; ISCX-VPN 0.9536, ISCX-Tor 0.9855; 10.82% ↑ on Telegram, 4.58% ↑ on ISCX-Tor. (Section 4.2; Tables 1-2)",
        "Hardware": "Single NVIDIA RTX 3080 GPU. (Section 4.1.3)",
        "FLOPs": "2.2e+3 FLOPs; 4.4e+1 parameters. (Table 4)",
        "Deployment limitations": "Static graph topology (non-optimal), cannot handle byte-level noise; unused temporal information in byte sequences. (Section 6)"
}, url['tfegnn'], "Full text; field locators in each value")
    detail('torfeatures', {
        "Traffic unit definition": "Bidirectional flow keyed by source/destination IP, source/destination port and protocol, generated with ISCXFlowMeter; flow duration is set to 10, 15, 30, 60 or 120 seconds, with 15s found optimal. (Section 3.1; Section 5.2)",
        "Input representation": "23 time-based features per flow: forward, backward and bidirectional inter-arrival times and active/idle durations (each mean, min, max, std), flow bytes per second, flow packets per second and duration; feature selection reduces these to 5 or 14 features in Scenario A and 10 or 15 in Scenario B. (Section 3.1; Sections 5.1 and 5.2)",
        "Architecture": "Weka implementations of ZeroR, C4.5 and KNN for the binary Scenario A and Random Forest, C4.5 and KNN for the eight-class Scenario B; feature selection via CfsSubsetEval+BestFirst and Infogain+Ranker. (Section 4.1)",
        "Training / evaluation datasets": "Self-generated, published Tor dataset captured between client and entry node via Whonix, with 8 traffic types from more than 18 applications (5631 Tor samples at the 15s timeout, Table 1); Scenario A merges it with the Draper-Gil et al. (2016) encrypted traffic dataset as nonTor (48123 samples at 15s), while Scenario B uses only the Tor dataset. (Section 3; Section 4; Table 1)",
        "Split strategy": "Datasets divided 80% for testing and 20% for validation; classifiers compared with 10-fold cross-validation on the 80% testing sets and finally evaluated on the 20% validation sets as supplied test sets. (Section 4.1)",
        "Metrics": "Precision and recall, measured as weighted averages during testing and reported per class with confusion matrices for validation. (Section 4.1)",
        "Reported results": "On the 15s validation dataset, Scenario A with C4.5 and Infogain+Ranker detects 93.4% of Tor samples at 94.8% precision and 99.4% of nonTor samples at 99.2% precision; Scenario B with Random Forest and Infogain+Ranker reaches weighted precision 0.843 and recall 0.838, best on VOIP and P2P. (Sections 5.1 and 5.2)",
        "Deployment limitations": "The classifier fails to obtain good results for the BROWSING, CHAT and E-MAIL classes, and accuracy depends on the flow timeout, with shorter values performing better and 15s optimal. (Section 5.2; Section 6)",
        "Leakage / shortcut risks": "Because every flow in a Tor capture is labelled as the single foreground application, the datasets contain label noise (flows of type X labelled as type Y) that lowers accuracy; web-based applications also leave BROWSING background traffic across all labels. (Section 3; Section 5.2)",
        "Version notes": "The conclusion says only 10 features are needed to detect Tor traffic; Section 5.1 reports that CfsSubsetEval+BestFirst reduces the 23 features to 5. (Section 5.1; Section 6)"
}, url['torfeatures'], "Full text; field locators in each value")
    detail('vpnfeatures', {
        "Traffic unit definition": "A sample is a bidirectional flow sharing source and destination IP addresses, source and destination ports, and transport protocol; the first packet determines direction. Flow durations are set to 15, 30, 60 and 120 seconds. (Section 4.1)",
        "Input representation": "ISCXFlowMeter extracts flow duration; mean, minimum, maximum and standard deviation of forward, backward and overall inter-arrival times, active times and idle times; and flow bytes and packets per second. (Section 4.1; Table 2)",
        "Architecture": "The proposed time-related features are classified using a C4.5 decision tree or K-nearest neighbours, implemented in Weka with default settings. (Section 4.2)",
        "Training / evaluation datasets": "The authors capture and publish a laboratory dataset covering browsing, email, chat, streaming, file transfer, VoIP and P2P, each with regular encrypted and VPN variants, yielding 14 traffic categories. (Section 3; Table 1)",
        "Split strategy": "Evaluation uses Weka's default settings with 10-fold cross-validation. (Section 4.2)",
        "Metrics": "Precision and recall are the evaluation metrics; results also report average precision across traffic categories. (Sections 4.2, 5.1 and 5.2)",
        "Reported results": "On the captured dataset, Scenario A VPN detection using C4.5 with a 15-second flow timeout achieves precision of 0.89 for VPN and 0.906 for non-VPN. (Section 5.1; Figure 2)",
        "Latency": "For traffic-type classification, the reported average response time is approximately 15.011 seconds for kNN and 16.491 seconds for C4.5, including flow collection, feature extraction and classification. (Section 4.1, response-time calculation)",
        "Measurement scope": "Response time comprises the configured flow duration, feature-extraction time and machine-learning classification time. (Section 4.1)"
}, url['vpnfeatures'], "Full text; field locators in each value")
