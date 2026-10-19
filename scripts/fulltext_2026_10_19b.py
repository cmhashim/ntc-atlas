"""Task 21 (2026-10-19): full-text extraction for the 12 discovery papers.
Drafted by four models (Codex, GLM, Gemini, Mistral; one per paper, see MODEL), each value with a
verbatim quote; Claude checked every quote and number against corpus/ PDFs and corrected or dropped
what did not match. Each value ends with its own locator."""

MODEL = {
 "shortcutgen": "Codex",
 "netcofi": "Codex",
 "curvtail": "Codex",
 "distilshortcut": "GLM",
 "dpft": "GLM",
 "pmpnet": "GLM",
 "netagent": "Gemini",
 "scsm": "Gemini",
 "netlexicon": "Gemini",
 "supclgnn": "Mistral",
 "vfrdad": "Mistral",
 "joivcompare": "Mistral"
}


# Catalogued collections each paper names in its full text, with that paper's own locator.
DATASETS = {
    'netagent': (['cicids2017', 'cicids2018', 'iscxvpn', 'mawi'], 'Section 4.1; Table 2'),
    'shortcutgen': (['cstnet', 'iscxvpn', 'ustc'], 'Section IV-A(a); Table I'),
    'netlexicon': (['cstnet', 'cipherspectrum', 'iscxvpn', 'ustc', 'mawi'], 'Section 4.1; Table 3'),
    'netcofi': (['cipherspectrum', 'cstnet', 'iscxtor', 'iscxvpn', 'ustc', 'ctu13'], 'Section IV-A(a)'),
    'pmpnet': (['iscxvpn', 'ustc'], 'Section 4.1; Table 1'),
}


def extract(detail, P, D=()):
    for p in P:
        if p['id'] in DATASETS:
            p['datasets'] = list(dict.fromkeys(p['datasets'] + DATASETS[p['id']][0]))
    for d in D:
        d['papers'] = [p['id'] for p in P if d['id'] in p['datasets']]
    url = {p["id"]: p["url"] for p in P}
    detail('curvtail', {
        "Traffic unit definition": "Samples are bidirectional flows grouped by five-tuple; the model uses up to 64 packets per flow. (Section 3.1, Datasets and baselines; Implementation)",
        "Input representation": "The packet view combines mixed-resolution discrete length tokens with direction, log-transformed inter-arrival time and position embeddings. The byte view embeds upstream and downstream bytes separately and compresses them into non-overlapping patches using a strided convolution. (Section 2.1, Equation (1))",
        "Packets / bytes": "Inputs contain up to 64 packets per flow and 256 bytes per direction. (Section 3.1, Implementation)",
        "Preprocessing / anonymisation": "After bidirectional five-tuple grouping, flows with fewer than five packets are removed. Length tokenisation preserves exact identities within a bounded range and coarsens larger lengths. (Sections 3.1 and 2.1)",
        "Architecture": "Separate packet and byte encoders use gated residual dilated convolutions with Lorentz logarithmic and exponential maps; packet features use learned-query attention pooling and byte features use masked mean pooling. Their projected concatenation is classified by trainable Lorentz prototypes with shared learnable curvature, alongside an auxiliary packet-length retention head. (Sections 2.2 and 2.3, Equations (2)–(3); Figure 2)",
        "Parameters": "The default model has 0.84M parameters for 300 classes and 0.82M for 100 classes, with the difference confined to the classification head. (Figure 4 caption)",
        "Fine-tuning objective": "Training from scratch jointly minimises flow-level cross-entropy and auxiliary cross-entropy predicting observed length tokens from packet features before pooling. The retention task uses unmasked, uncorrupted tokens and does not modify class priors or prediction logits. (Sections 2.2 and 2.3, Equation (3); Section 3.1)",
        "Training / evaluation datasets": "DataCon-Website contains 100 website classes over encrypted tunnels and 85,146 retained flows; NUDT-Mobile contains 300 mobile-app classes and 1,282,557 retained flows. Both retain naturally long-tailed class frequencies. (Section 3.1, Datasets and baselines; Table 1)",
        "Split strategy": "All methods share a fixed, class-stratified 7:1:2 training/validation/test split at flow level for closed-set classification; checkpoints are selected using validation Macro-F1. (Section 3.1, Datasets and baselines; Implementation)",
        "Metrics": "ACC and Macro-F1 cover all classes; Tail-F1 averages per-class F1 over tail classes, while Tail-R measures the fraction of correctly classified test flows whose true labels are tail classes. Classes ranked by decreasing training frequency form head/body/tail groups containing 50%/30%/20% of classes, and main results average seeds 42, 2027 and 3407. (Section 3.1, Metrics and runs; Table 1 caption)",
        "Reported results": "On NUDT-Mobile, three-seed mean ACC, Macro-F1 and Tail-F1 are 96.70%, 93.48% and 85.70%; on DataCon-Website they are 73.53%, 66.66% and 46.30%, respectively. (Table 1, Curv-Tail row; Section 3.2)",
        "Hardware": "Efficiency profiling uses an RTX 4090 with FP32 and batch size 256. (Section 3.4; Abstract)",
        "Measurement scope": "Efficiency profiling measures amortised model forward time and retains the auxiliary retention head; counted MACs exclude element-wise operations. (Section 3.4)",
        "Latency": "Amortised batch forward time 0.1359 ms per flow (median batch time divided by batch size), offline. (Section 3.4)",
        "Throughput": "10.2× MM4Flow’s batch inference throughput in 300-class profiling (RTX 4090, FP32, batch 256). (Section 3.4)"
}, url['curvtail'], "Full text; field locators in each value")
    detail('distilshortcut', {
        "Traffic unit definition": "Flow-level: each TLS flow is one sample, represented by its first 30 packets. (Section III-A (Inputs))",
        "Input representation": "Three per-packet sequences (inter-packet time, direction, size) over the first 30 packets, plus 12 flow statistics and a 32-bin packet-size histogram (44 tabular features); sequences and statistics are scaled with transforms fitted on each training window only. (Section III-A (Inputs))",
        "Packets / bytes": "First 30 packets per flow, used only through timing, direction and size; no payload or byte budget is stated. A sensitivity analysis also reports flows with at least five packets (94.0% of test flows). (Section III-A (Inputs); Section IV-A)",
        "Preprocessing / anonymisation": "Server name, IP addresses, ports, autonomous system and JA3 fingerprint are excluded from the inputs, so the classifier sees what it would see under Encrypted Client Hello; scaling transforms are fitted per training window. Each test flow carries a duplicate flag (64-bit hash of the scaled sequence) and 1.8% of test flows exactly occur in their training window, removed in a sensitivity analysis. (Section III-A (Inputs; Time structure); Section IV-A)",
        "Architecture": "Student: multimodal 1D-CNN with three convolutions (48, 96, 96 channels; kernels 5, 5, 3) over the packet sequences pooled by mean and max, a 64-unit layer over the flow statistics, a 128-unit shared layer with dropout 0.1 and a linear classifier. Teacher A is a five-member ensemble of mm_cesnet_v2 multimodal CNNs (mean of member softmax outputs); Teacher B is a single wider network of the same family (three convolutional blocks of 400/600/600 channels, two 450-unit statistics layers, a 1,200-unit shared layer); an exploratory Teacher C is a transformer encoder over the packet sequence. (Section III-B (Models); Section V-B)",
        "Parameters": "Student 101,190 parameters (101k), 22× smaller than one teacher member and 112× smaller than the ensemble; Teacher A members 2.26M each (11.3M as an ensemble), Teacher B 10.3M, exploratory transformer Teacher C 3.5M. (Section III-B; Section V-B; Table II)",
        "Fine-tuning objective": "There is no pretraining or fine-tuning; students are trained from scratch. Hinton KD minimises αT²KL(teacher‖student) + (1−α)CE with α = 0.9 at T ∈ {1, 4}; controls are direct cross-entropy, post-hoc temperature scaling, label smoothing ε = 0.05 and proxy-Dirichlet EnDD with reverse-KL (precision capped at 10⁴). All networks use AdamW (learning rate 10⁻³, weight decay 10⁻⁴), a one-cycle schedule with 10% warm-up, batch size 1,024 and bf16 autocast; teachers 10 epochs, students 20. (Section III-C (Training Conditions); Table I)",
        "Training / evaluation datasets": "CESNET-TLS-Year22 only: the S subset (25M flows) of one year (2022) of TLS flows from the Czech national research network, accessed via cesnet-datazoo 0.2.0, with 180 services labelled from the server name. 102 services are known classes; held-out unknowns differ between validation (far: Music and Videoconferencing, 8 services, plus 5 near) and test (far: Search and Social, 11 services, plus 8 near), and 46 further services are excluded, mostly for insufficient or inconsistent volume. (Section III-A (Dataset; Known and unknown services))",
        "Split strategy": "Time-ordered, three replicates by training start date: training on weeks 11-14, 24-27 and 37-40 (1.89M, 1.37M and 1.35M known flows), validation on the following week (200k known flows plus all validation-unknown flows), then consecutive 4-week test windows to week 52, giving 9, 6 and 3 windows (18 total), each a stratified sample of 100k known and 100k unknown flows at 3.5 to 35.3 weeks after training. The service split (102 known, seed 2022) was generated once before any model was trained. (Section III-A (Time structure; Known and unknown services))",
        "Metrics": "Closed-set macro-F1 (macro averaging stated); unknown-detection AUROC and FPR at 95% TPR under two unknown-scores, the energy score (log-sum-exp of the logits) and maximum softmax probability (MSP), with known flows as positives; OSCR; ECE (15 bins), NLL and Brier score before and after temperature scaling; AURC; and Spearman correlation of per-flow energy scores for inheritance. (Section III-D (Outcomes))",
        "Reported results": "Averaged over the 18 test windows (Table II): direct student 0.806 macro-F1 and 0.835 energy AUROC; kdA (T=1) 0.806 and 0.834 (indistinguishable from direct and directTS); kdA4 (T=4) 0.790 and 0.809; ls 0.797 and 0.814; enddA 0.801 and 0.742 (worst energy detector); Teacher A 0.860 and 0.836. Teachers are 4.8 to 7.1 macro-F1 points more accurate but only 0.001 energy AUROC better at detection; H1 is supported (kdA4 +0.007, kdB4 +0.026 own-teacher shift, Holm p = 0.009) and H3 reversed (teacher-student energy AUROC slope of -0.0004 per week); under feature-space scores Teacher A is 0.073 Mahalanobis AUROC above direct, kdA4 recovers +0.076, and label smoothing beats kdA4 by +0.011. (Table II; Table III; Section IV; Section V-A)",
        "Hardware": "Inference was measured on a laptop CPU (AMD Ryzen 7 5800H, 8 cores) as a stand-in for an edge device; no training or GPU hardware is stated. (Section IV-E; Table VII)",
        "Measurement scope": "The efficiency numbers cover offline model forward-pass inference only: per-flow latency at batch size 1 on one thread, throughput at batch size 1,024, and serialised model size; they do not cover feature extraction, capture or a live pipeline. The teachers could not be exported to ONNX Runtime, so only the student was timed in ONNX, and the re-tuned XGBoost was timed in a separate session. (Table VII caption; Section IV-E)",
        "Deployment limitations": "Stated: novelty is simulated (no service first appears mid-year), the study is one dataset, one network, one year, and the confirmatory grid uses a single teacher architecture at two widths, with the transformer teacher exploratory on one start date. Also stated: natural shortcut fields (server IP, ASN, JA3) were excluded from the inputs, not tested; the shortcut experiment plants a synthetic feature on the validation week at a single student width; H1's support rests more on kdB4 than kdA4 (kdA4 null at start date 11 unexplained); baselines and deployment cost were measured on the validation week and a laptop CPU; deposited per-flow score files store MSP in float16, which saturates confident flows; the feature-distillation arm carries an untuned loss weight (β = 100). (Section VI (Limitations); Section V-G; Section VII)",
        "Version notes": "Preprint, September 2026 (arXiv:2609.31141v1, 25 Sep 2026), pre-registered at OSF and frozen at repository commit fa8f718 after a pilot and validation-only design phase, with all Section V analyses added after the confirmatory results were known. Timing numbers come from two sessions: the text quotes the student at 0.08 ms while Table VII gives 0.082 ms p50, and the re-tuned XGBoost comparison uses its own session (14.4 ms against 0.072 ms for the student). (Front page and footer; Section III; Section IV-E; Table VII)",
        "Latency": "Student in ONNX Runtime: 0.082 ms p50 and 0.160 ms p99 per flow (batch size 1, one thread); Teacher A ensemble 19.093 ms p50; XGBoost 41.606 ms. Offline forward pass only. (Table VII; Section IV-E)",
        "Throughput": "Student 21,201 flows/s on one thread (ONNX Runtime); PyTorch student 39,418 flows/s on all cores; Teacher A 161 flows/s. (Table VII)",
        "Memory": "Serialised weights: student 0.4 MB, Teacher A 45.4 MB, Teacher B 41.3 MB, XGBoost 244.4 MB. (Table VII)"
}, url['distilshortcut'], "Full text; field locators in each value")
    detail('dpft', {
        "Traffic unit definition": "The unit is the bidirectional session (packets in temporal order, five-tuple used only for reconstruction); sessions are partitioned into direction-continuous bursts for pre-training, and each fine-tuning sample takes the session's first 10 packets. (Section 3.1; Eqs. (2)-(3); Table 2)",
        "Input representation": "Sanitized Byte-Bigram tokens generated within each packet, with a [PKT] boundary token between adjacent packets; [CLS] is prepended and sequences are padded or truncated to a maximum encoder length of 648 tokens. (Section 3.1; Algorithm 1; Table 2)",
        "Packets / bytes": "First 10 packets per session (K=10) with at most 64 retained sanitized bytes per packet (M=64), giving a maximum encoder input of 648 tokens. (Section 3.1; Algorithm 1; Table 2)",
        "Preprocessing / anonymisation": "PCAPs are standardised with editcap and segmented into bidirectional sessions with SplitCap; link-layer addresses, IP addresses, ports and plaintext host or domain fields are replaced with zero-valued bytes, affected checksums are normalised, and identifiers are not given to the model. (Section 3.1)",
        "Architecture": "A 12-layer Transformer encoder with hidden size 768, 12 self-attention heads and feedforward size 3072 is shared between pre-training and fine-tuning; fine-tuning adds a Dynamic Weighting module for token and positional embedding fusion, a Mask-aware Multi-Head Attention Pooling module, then a ReLU plus fully connected classifier. (Section 4; Table 2; Sections 3.3.1-3.3.3)",
        "Parameters": "Full DPFT has 135.10M parameters (22.67 GFLOPs per sample); the variant without MHAP has 132.73M and the variant without DW has 134.11M. (Section 4.8; Table 9)",
        "Pretraining objective": "Masked Burst Prediction (contiguous span masking covering about 20% of retained content tokens; affected tokens masked with 80% probability, replaced by a random token with 10% and kept unchanged with 10%) and Burst Structural Discrimination (binary cross-entropy on adjacent burst pairs versus inter-session, non-adjacent and reversed-order negatives) are jointly optimised with equal weight (λ_BSD = 1). (Section 3.2)",
        "Pretraining datasets": "About 30 GB of unlabeled traffic: 15 GB of real-world CSTNET traffic plus approximately 15 GB from the benchmark datasets (ISCX-VPN-App, ISCX-VPN-Service, USTC-TFC 2016); only training-partition sessions are used, over 500,000 steps with checkpoints every 10,000 (AdamW, learning rate 5×10^-5). (Section 4.1; Section 4; Section 3.1; Table 2)",
        "Fine-tuning objective": "Supervised multi-class cross-entropy over traffic categories; the transferred encoder, DW, MHAP and MLP classification head are jointly optimised for 30 epochs with AdamW (fine-tuning learning rate 2×10^-5, batch size 32). (Section 3.3.3; Table 2)",
        "Training / evaluation datasets": "CSTNET-TLS 1.3 (120 classes, 46,372 flows, 581,709 packets), ISCX-VPN-App (17 classes, 2,329 flows, 77,163 packets), ISCX-VPN-Service (12 classes, 3,694 flows, 60,000 packets) and USTC-TFC 2016 (20 classes, 9,853 flows, 97,115 packets). (Section 4.1; Table 4)",
        "Split strategy": "Session-level partitioning into 80% training, 10% validation and 10% test per dataset (8:1:1); all samples from one session stay in the same subset and validation or test sessions are excluded from pre-training; evaluation is within-dataset and closed-set. (Section 3.1; Table 2; Section 4.6)",
        "Metrics": "Accuracy plus macro-averaged precision, recall and F1 (Pr_Macro, Rc_Macro, F1_Macro). (Section 4.2)",
        "Reported results": "Macro-F1 of 93.10% on CSTNET-TLS 1.3, 97.92% on ISCX-VPN-App, 95.65% on ISCX-VPN-Service and 98.87% on USTC-TFC 2016, with accuracies of 93.01%, 97.95%, 95.66% and 98.87% respectively, exceeding eleven baselines under a within-dataset closed-set protocol. (Abstract; Tables 5-6)",
        "Hardware": "Pre-training on four NVIDIA RTX 2080Ti GPUs (11 GB each); downstream fine-tuning on one NVIDIA RTX 4060 GPU (8 GB). (Section 4 (experimental setup))",
        "Measurement scope": "The efficiency numbers cover offline model inference under the reported hardware and experimental configuration only; system behaviour under operational deployment conditions has not been evaluated. (Section 4.8)",
        "Deployment limitations": "Results are limited to within-dataset closed-set benchmarks and do not establish robustness to temporal or cross-domain shifts, unseen classes or deployment conditions; USTC-TFC 2016 results are not evidence of performance on contemporary encrypted traffic; QUIC was not evaluated. (Section 4.9; Abstract; Section 4.6.2)",
        "Version notes": "Journal Pre-proof (marked-up revised manuscript) for Computer Networks, received 7 June 2026, revised 4 October 2026, accepted 5 October 2026; the version will undergo further copyediting and is not yet the Version of Record. (Cover page)",
        "Latency": "12.56 ms per sample at batch size 1, offline (30 warm-up, 200 timed iterations). (Section 4.8; Table 9)",
        "Throughput": "289.07 samples/s at batch size 32, offline. (Section 4.8; Table 9)",
        "Memory": "526.75 MB peak memory at batch size 1. (Section 4.8; Table 9)",
        "FLOPs": "22.67 GFLOPs per sample. (Section 4.8; Table 9)"
}, url['dpft'], "Full text; field locators in each value")
    detail('joivcompare', {
        "Traffic unit definition": "Flow; 20 packets per flow sequence. (Table I; Section II.C)",
        "Input representation": "Behavioral telemetry: encrypted payload descriptors, TCP and UDP headers, jitter metrics, bandwidth logs, microsecond-resolution timestamps. (Section II.B)",
        "Packets / bytes": "20 packets per flow sequence. (Table I)",
        "Preprocessing / anonymisation": "Min-Max Normalization (0-1 scaling), Traffic Burstiness Index, IQR-based outlier removal. (Section II.B.1)",
        "Architecture": "Transformer with 64-dimensional learned embedding, 8 multi-head attention channels, 4 feed-forward hidden layers, 128 internal feature dimensions, ReLU activation, 0.10 dropout, positional encoding. (Table I; Section II.C)",
        "Parameters": "10,753 parameters. (Table IV; Table V)",
        "Training / evaluation datasets": "Jabatan Data Negara (JDN) Malaysia real-world telemetry dataset; 12,000 encrypted traffic flows across 648 application classes; 5,600 jitter samples (2-25 ms), 5,400 bandwidth samples (0.5-8 Mbps). (Abstract; Section II.A; Section II.B)",
        "Split strategy": "Flow-level stratified sampling; 70% training (8,400 samples), 15% validation (1,800 samples), 15% testing (1,800 samples). (Section II.B.2)",
        "Metrics": "Accuracy, Precision, Recall, balanced F1 Score; Throughput (Gbps), Inference Latency (microseconds). (Section II.D)",
        "Reported results": "Transformer: 99.60% accuracy, 12.4 Gbps throughput, 10,753 parameters, 21 epochs; baselines: ANN 99.83% 8.2 Gbps 150,147 params, CNN 65.13% 9.5 Gbps 189,756 params, RNN 99.85% 6.8 Gbps 2,803 params. (Abstract; Table IV; Table V)",
        "Hardware": "11th Gen Intel Core i7-1165G7 CPU, 16GB RAM, NVIDIA GeForce RTX 3060 (16GB GDDR6), CUDA v11.7, cuDNN 8.5, Python 3.10, PyTorch. (Section II.E)",
        "Measurement scope": "Classification correctness and runtime operational efficiency under production workloads. (Section III.C)",
        "Deployment limitations": "Transformer quadratic overhead with sequence length may saturate edge memory; RNN has sequential-processing bottleneck but is ultra-lightweight (2,803 parameters). (Section III.C)"
}, url['joivcompare'], "Full text; field locators in each value")
    detail('netagent', {
        "Traffic unit definition": "Flows within a capture, where traffic is grouped into flows and converted into a unified multi-view feature matrix. (Section 3.1; Section 3.2)",
        "Input representation": "A unified multi-view feature matrix stacking flow-level vectors across over 50 views, encompassing packet-length statistics, inter-arrival times, flow statistics, protocol fields, TCP flags, and packet-length distributions. (Section 3.2)",
        "Packets / bytes": "Payload content is excluded from the feature matrix because traffic is largely encrypted and payload features drift across application versions. (Section 3.2)",
        "Architecture": "An agentic framework coordinating three LLM-based agents (decision maker, planner, and executor) backed by a 157-tool library across five functional layers (L1 data reading, L2 feature extraction, L3 feature construction, L4 attack characterization, L5 analysis models), an attack knowledge base, a persistent Python code execution sandbox, and a three-tier memory (episodic, pattern, knowledge). (Section 3.1; Section 3.3; Section 3.4; Section 3.6)",
        "Training / evaluation datasets": "Nine evaluation benchmarks: UNSW-NB15 (2.5M records), CIC-IDS2017 (2.8M records), CIC-IDS2018 (16.2M records), CICIoT2023 (46.8M records), CIC-DDoS2019 (50M+ records), ISCX-VPN2016 (9.8K records), DF2018 (140K records), CAIDA AS (70M+ records), and DGArchive (100M+ records), alongside real-world background traffic from MAWI/WIDE (200M+ records). (Section 4.1; Table 2)",
        "Split strategy": "An 80/20 train/test split per dataset, with reported results averaged over 10-fold cross-validation. (Section 4.1)",
        "Metrics": "F1 score. (Section 4.1)",
        "Reported results": "NetAgent achieves an F1 score of 0.9863 on UNSW-NB15, 0.9995 on CIC-IDS2017, 0.9999 on CIC-IDS2018, 0.9998 on CICIoT2023, 0.9999 on CIC-DDoS2019, 0.9242 on ISCX-VPN2016, 0.9965 on DF2018, 1.00 on CAIDA AS, and 0.9999 on DGArchive. (Section 4.2; Table 3; Table 8)",
        "Deployment limitations": "The framework is restricted from real-time traffic processing, its capabilities are bounded by the coverage of its tool action space and attack knowledge base, and its current tool library lacks a byte-level encoder for payload patterns. (Section 4.2; Section 5)",
        "Latency": "Agent reasoning (LLM calls and several analyses per capture) dominates latency; the authors state NetAgent is not a real-time traffic processor. (Section 5)"
}, url['netagent'], "Full text; field locators in each value")
    detail('netcofi', {
        "Traffic unit definition": "The main sample is a fixed flow window containing the first packets of a flow. The deployment assembler groups both directions using a canonical bidirectional five-tuple and constructs an input once five packets are available. (Sections III-B and IV-H)",
        "Input representation": "Concatenated packet header and payload bytes are projected into stride tokens by a one-dimensional convolution. Tokens also receive metadata features describing timing, length, direction, TCP flags, protocol and position. (Section III-B, Equation (1); Table I)",
        "Packets / bytes": "The default input uses five packets, with each packet's header truncated or padded to 80 bytes and payload truncated or padded to 240 bytes. (Section III-B)",
        "Preprocessing / anonymisation": "Continuous side features are normalised using training-set statistics, with the same transformation applied to validation and test data. The auxiliary strict-split analysis clears IP addresses and ports, retains flows with at least five packets for flow classification, and balances training and validation classes by undersampling. (Sections III-B and IV-F)",
        "Architecture": "Learned importance scores select seed-token neighbourhoods for a fine Mamba branch, while anti-importance weighted pooling compresses the full sequence for a separate coarse Mamba branch. A coarse-summary channel gate modulates fine features before pooled branch outputs are concatenated for classification. (Sections III-C and III-D, Equations (2)–(10); Figure 2)",
        "Fine-tuning objective": "Downstream multi-budget training combines supervised classification loss, distillation from the full-budget prediction and a penalty aligning mean importance with the requested seed-token ratio. Each minibatch evaluates endpoint budgets and uniformly sampled intermediate budgets. (Section III-E, Equations (11)–(14); Section IV-A(d))",
        "Training / evaluation datasets": "The main datasets are CipherSpectrum, CSTNET-TLS1.3, ISCXTOR2016, ISCXVPN2016, USTC-TFC2016 and CTU-13, using balanced subsets for the Tor and VPN datasets and stratified sampling for USTC-TFC2016. Auxiliary strict-split tasks are VPN-app with 16 classes and TLS-120 with 120 classes. (Sections IV-A(a) and IV-F; Tables II, III and VI)",
        "Split strategy": "The main evaluation uses an 8:1:1 training/validation/test split; CTU-13 additionally keeps captures disjoint while preserving class proportions through proportional sampling. Auxiliary strict-split tasks partition at flow level so constituent packets remain in the same subset, with undersampling confined to training and validation. (Sections IV-A(a) and IV-F)",
        "Metrics": "Classification metrics are accuracy and Macro-F1; efficiency metrics are inference latency, throughput and peak GPU memory. Model throughput uses samples/s, while deployment pipeline throughput uses Mb/s. (Section IV-A(c))",
        "Reported results": "Without pretraining, Macro-F1 is 92.81% on ISCXTOR2016, 91.92% on ISCXVPN2016, 97.01% on USTC-TFC2016, 74.79% on CTU-13, 82.75% on CSTNET-TLS1.3 and 45.16% on CipherSpectrum. With pretraining, the corresponding scores are 94.48%, 94.40%, 97.38%, 74.51%, 89.35% and 61.69%. (Tables II and III, NetCoFi rows)",
        "Hardware": "Experiments use NVIDIA GeForce RTX 4090 GPUs with PyTorch 2.8.0 and CUDA 12.8; NetCoFi training uses FP32. (Section IV-A(d))",
        "Measurement scope": "Deployment batch throughput runs from DPDK-delivered packets to predictions, including flow aggregation, feature construction, routing and GPU inference, while excluding disk I/O and offline trace loading. Separate model inference timings include token selection and routing but exclude data loading. (Sections IV-H and IV-C(4))",
        "Deployment limitations": "Reducing the routing budget below the useful middle range causes substantial classification degradation. (Section IV-C(1))",
        "Throughput": "Mean batch throughput 43.42 Mb/s in the authors’ DPDK–GPU pipeline, against 26.42 Mb/s for NetMamba (1.64×). Model-only latency, throughput and GPU memory are measured separately after warm-up. (Sections IV-C(4), IV-H; Figures 6, 8)"
}, url['netcofi'], "Full text; field locators in each value")
    detail('netlexicon', {
        "Traffic unit definition": "Bidirectional flow defined by 5-tuple, ordered chronologically, parsed into bursts of consecutive same-direction packets and sliding windows of 5 consecutive bursts. (Section 3.1)",
        "Input representation": "Sequences of packet tokens with inserted [SEP] after each burst and [WIN] after every W bursts. Each packet token consists of 7 normalized features concatenated with 7 binary missing indicators to form a 14-dimensional vector, alongside separate embeddings for token types and positions. (Section 3.1; Appendix A)",
        "Packets / bytes": "Maximum sequence length of 256 tokens. Sliding windows contain 5 consecutive bursts. (Section 3.1; Section 4.1)",
        "Preprocessing / anonymisation": "SplitCap is used to extract bidirectional flows. Flows containing fewer than one complete window of 5 consecutive bursts are discarded. Explicit avoidance of raw IP addresses, port numbers, TTL, and raw IPID. (Table 2; Section 4.1)",
        "Architecture": "Four-layer causal transformer encoder with hidden size 192, feed-forward size 768, 16 attention heads, followed by a VQ-VAE discrete lexicon layer with a codebook of 128 codewords, and two projection heads for SFA. (Section 3.2; Section 4.1)",
        "Parameters": "1.9M parameters. (Section 4.4; Figure 8)",
        "Fine-tuning objective": "Cross-entropy loss on labeled flows using a pooled [WIN] representation passed through a task-specific classification head, trained in two stages (frozen backbone first, then joint end-to-end). (Section 3.5; Section 4.1)",
        "Training / evaluation datasets": "CSTNET (Web APP fingerprinting, 120 classes, 45.16K flows), CipherSpectrum (Web APP fingerprinting, 42 classes, 164.2K flows), ISCXVPN (Service type identification, 7 classes, 2.184K flows), and USTC-TFC (Malware detection, 17 classes, 114.3K flows). (Table 3)",
        "Split strategy": "Flow-level random split within each class using an 8:1:1 train:validation:test ratio with seed 42; all windows from the same flow remain in the same partition. (Section 4.1)",
        "Metrics": "Accuracy, macro-precision, macro-recall, and Macro-F1. (Section 4.1)",
        "Reported results": "ISCXVPN: 0.8267 accuracy, 0.8034 Macro-F1; USTC-TFC: 0.9889 accuracy, 0.9547 Macro-F1; CSTNET: 0.8838 accuracy, 0.8637 Macro-F1; CipherSpectrum: 0.9104 accuracy, 0.9002 Macro-F1. (Tables 4 and 5)",
        "Hardware": "NVIDIA A100 GPUs. (Section 4.1)",
        "Measurement scope": "Measurements reflect GPU neural computation for model fine-tuning and batch inference, but exclude full encoding pipeline costs such as state assignment generation. (Section 5)",
        "Deployment limitations": "Performance relies on recurring observable behavior consistency, which changes across varying network conditions or protocol implementations, requiring adaptation of encoder and codebook; producing contextual window representations still requires neural computation. (Section 5)",
        "Pretraining objective": "State Transition Prediction (token type prediction and packet feature regression), codebook commitment with EMA updates, and Statistical Feature Alignment (InfoNCE over 37 window statistics). (Section 3.5)",
        "Pretraining datasets": "1,057,331 flows (about 86.34 million packets) from MAWI and VisQUIC. (Section 4.1)",
        "Latency": "11.1 ms offline batch inference latency at batch size 32; fine-tuning 3.0 minutes per epoch. (Section 4.4)",
        "Memory": "0.9 GB GPU memory at batch size 32. (Section 4.4)"
}, url['netlexicon'], "Full text; field locators in each value")
    detail('pmpnet', {
        "Traffic unit definition": "Packet-level: individual packets serve as the classification units, with each captured flow segmented into single packets during preprocessing. (Sections 3.2 and 4.1)",
        "Input representation": "A packet is decomposed into a fixed-length header byte sequence encoded with byte plus positional embeddings, and a payload represented as a normalised 256-dimensional byte-value histogram; an FFT of the histogram yields a 512-dimensional frequency-domain vector for the payload branch. (Sections 3.2-3.3)",
        "Packets / bytes": "One packet per sample; the header is standardised to 64 bytes (longer truncated, shorter zero-padded), while the payload is not segmented or truncated and all valid payload bytes are counted into the histogram. (Section 3.2)",
        "Preprocessing / anonymisation": "Duplicate and empty packets are removed, IP and MAC addresses are erased for anonymisation, and control packets carrying only SYN, ACK or FIN flags without payload are discarded; header lengths are then standardised by cropping or zero-padding. (Section 3.2)",
        "Architecture": "Dual-branch design: header branch with multi-scale depthwise-separable 1D convolutions (kernels 3 and 5), a residual block with SE attention, a GLU, a two-layer Transformer encoder and global average pooling to a 128-d header vector; payload branch with FFT over the histogram and a two-layer MLP to 128 dimensions; bidirectional multi-head attention fusion, then a prototype classifier with cosine margin and similarity-threshold unknown rejection. (Sections 3.3-3.5)",
        "Fine-tuning objective": "Episodic 5-way-10-shot training minimises cross-entropy loss with label smoothing (0.1) over margin-penalised, temperature-scaled cosine similarities to class prototypes, using Adam with warmup and cosine-annealing scheduling and early stopping. (Sections 3.5 and 4.4)",
        "Training / evaluation datasets": "ISCX VPN-nonVPN (14 classes, 79,315 samples, 16.3 GB) and USTC-TFC2016 (10 classes, 172,048 samples, 3.2 GB); open-set experiments designate a subset of categories as unknown, excluded from training and used only at test time. (Section 4.1; Table 1)",
        "Split strategy": "Random packet-level split into training, validation and test sets at 8:1:1; open-set classes are wholly excluded from training and introduced only at test time. (Section 4.1)",
        "Metrics": "Accuracy, precision, recall and F1-score for closed-set classification; TPR, FPR and AUROC for open-set rejection; no averaging scheme (macro or weighted) is stated. (Section 4.2)",
        "Hardware": "Windows 11 workstation with a 12th Gen Intel Core i5-12500H processor (12 cores, 16 threads), 32 GB DDR5 4800 MHz RAM and an NVIDIA GeForce RTX 3050 Laptop GPU (4 GB VRAM); Python 3.10.13 with PyTorch and CUDA. (Section 4.4)",
        "Measurement scope": "Efficiency numbers cover per-packet model inference latency only; preprocessing cost, memory usage and end-to-end pipeline throughput are not reported. (Section 4.8; Table 6)",
        "Deployment limitations": "The authors acknowledge PMP-Net is slightly slower per packet than the lightweight ECM (1.57 ms) and SAM (2.56 ms) baselines, though it is more accurate. (Section 4.8)",
        "Reported results": "Accuracy 98.9% on ISCX VPN-nonVPN (precision 0.99, recall 0.988, F1 0.989) and 99.2% on USTC-TFC2016 (precision 0.996, recall 0.994, F1 0.995). Open-set AUROC peaks at 0.8243 at similarity threshold 0.70. (Abstract; Tables 2–3; Section 4.6)",
        "Latency": "Average model inference latency 5.75 ms per packet on the authors’ workstation; no throughput or memory figures. (Section 4.8; Table 6)",
        "Version notes": "The ablation text reports 99.50% USTC-TFC2016 accuracy for the full model, while the abstract and Table 3 report 99.2%. (Section 4.5; Table 3)"
}, url['pmpnet'], "Full text; field locators in each value")
    detail('scsm', {
        "Traffic unit definition": "Encrypted packet traces containing timestamped packet directions, divided into N non-overlapping windows of length w sampled from 5 to 50 ms, with N equal to 2700 for single-tab tasks and 7200 for multi-tab tasks. (Section IV-B; Section V-A.2)",
        "Input representation": "Direction-only Windowed Traffic Counting Matrix (WTCM) transformed element-wise by log(1 + M), forming a 4 by N matrix recording outgoing counts, incoming counts, inter-window gap, and packet cluster count. (Section IV-B; Algorithm 1)",
        "Architecture": "A 4 by 1 convolution projecting each window to embedding dimension 512, followed by four causal convolutional blocks with temporal max pooling (kernel size 5, dropout 0.1), sinusoidal positional embeddings, three Mamba2 blocks with maximum drop-path rate 0.2, temporal mean pooling, and a linear head. (Section IV-D.1; Section V-A.2)",
        "Fine-tuning objective": "Cross-entropy loss jointly fine-tuning the pretrained encoder and a task-specific linear classification head on a small labeled support set. (Section III-B)",
        "Training / evaluation datasets": "Pretrained on GTT23 (weeks 1 to 7) or Swallow D1 (100 websites, 100 traces each); evaluated on GTT23 weeks 8 to 13 (200 websites), Swallow D2 to D7, DFSet (95 websites), simulated W-TSet (100 websites), k-NNSet (100 websites), R-PSet (265 websites), Open-World DFSet (40,000 unmonitored traces), ARESSet (2 to 5 tabs, 100 monitored websites), and Defended DFSet. (Section V-A.1)",
        "Split strategy": "GTT23 temporal drift uses 10 labeled traces per website for adaptation and 5 disjoint traces per website for testing; Swallow uses 10 labeled traces per website for adaptation and 90 for testing; single-tab cross-domain uses 10-shot adaptation; Open-World DFSet uses 10 labeled traces per monitored website and 10 unmonitored traces; multi-tab uses 3,000 labeled traces. (Section V-A.1)",
        "Metrics": "Single-tab classification uses accuracy and macro-F1, with Accuracy@3 for GTT23; open-world uses r-precision (pi_r with r = 20) and recall; multi-tab evaluation uses P@k and MAP@k. (Section V-A.4)",
        "Hardware": "Four NVIDIA RTX 4090 GPUs. (Section V-A.2)",
        "Reported results": "Six-week average Accuracy@3 on GTT23 is 79.3% (77.0–81.8% per week). Closed-world cross-domain transfer: average macro-F1 78.8% pretrained on GTT23 and 81.3% pretrained on Swallow D1, against 67.5% for the strongest supervised baseline (RF). (Sections V-B, V-D; Table II)",
        "Pretraining objective": "Symmetric cross-view contrastive loss over views built by Segmentation, Combination, Scaling and Masking. (Section IV-D)",
        "Pretraining datasets": "First 7 weeks of GTT23, or scenario D1 of Swallow (two separate pretraining sources). (Section V-A)"
}, url['scsm'], "Full text; field locators in each value")
    detail('shortcutgen', {
        "Traffic unit definition": "Packet experiments use individual packets; flow experiments construct samples from packets belonging to the same bidirectional parent flow. (Section III-A; Table I)",
        "Input representation": "The field-text view uses field–value tokens encoded as 10,000-dimensional TF-IDF features with 1–3-grams and a LinearSVC classifier. Byte-based experiments use model-specific packet or flow representations. (Sections III-A and IV-A(a); Table I)",
        "Packets / bytes": "The principal flow inputs contain the first five packets of each parent flow. (Section III-A; Table I)",
        "Preprocessing / anonymisation": "Cumulative masking removes MAC addresses and frame.number, then IP addresses including IPv6, then transport ports, with independent retraining for each condition. Separate byte transformations compare original addresses, per-flow IP remapping and IP zeroing under test-only and matched training–test processing. (Sections III-B and III-D)",
        "Training / evaluation datasets": "The evaluation uses CSTNET-TLS 1.3, ISCXVPN and USTC-TFC. (Section IV-A(a); Table I)",
        "Split strategy": "Packet experiments compare random packet assignment with grouping by undirected IP pair, source IP or bidirectional parent flow. Flow experiments compare random flow assignment with initiator-disjoint partitioning that preserves parent-flow integrity. (Section III-C)",
        "Metrics": "Macro-F1 is the primary metric for masking, field diagnostics and transformation experiments; controlled sharing experiments report accuracy or accuracy differences. (Section IV-A(b))",
        "Reported results": "In the controlled source-IP experiment, complete overlap produces accuracy gains of 33.29 percentage points for LinearSVC and 32.05 points for ET-BERT under the original-field condition. (Section IV-D(a); Figure 3(a))"
}, url['shortcutgen'], "Full text; field locators in each value")
    detail('supclgnn', {
        "Traffic unit definition": "bidirectional or session flows segmented using five-tuple identifiers. (Section 2.1; Section 3.1)",
        "Input representation": "raw byte content and packet length sequence per flow. (Section 3.1)",
        "Packets / bytes": "first 10 packets per flow; 40 header bytes and 90 payload bytes per packet with 256-padding and dummy packets for short flows. (Section 3.1; Section 4.2.2; Section 4.3.3)",
        "Preprocessing / anonymisation": "IP and port removal from headers; first 10 packet selection; header/payload truncated to 40/90 bytes with 256-padding; dummy packets for flows with fewer than 10 packets; filtering empty-payload and outlier flows. (Section 3.1; Section 4.2.2)",
        "Architecture": "multi-scale CNN for packet-level representation, adaptive gated header/payload fusion, Traffic Distribution Graph construction, four GraphSAGE layers, supervised contrastive learning. (Section 3; Section 3.4.2)",
        "Training / evaluation datasets": "ISCX-VPN2016 (6 classes), ISCX-Tor2016 (8 classes), USTC-TFC2016 (20 classes), MOBILE-APP (8 mobile apps). (Section 4.1)",
        "Metrics": "accuracy, macro-averaged precision, recall, and F1 score. (Section 4.2.1)",
        "Hardware": "Intel Core i9-10850K CPU at 3.60 GHz, NVIDIA RTX 3080 GPU. (Section 4.2.2)",
        "Measurement scope": "FLOPs and parameter counts measure computational complexity only. (Section 4.7)",
        "Deployment limitations": "FLOPs and parameter counts cannot fully reflect practical deployment efficiency. (Section 5)",
        "Reported results": "Accuracy / F1: ISCX-VPN2016 0.9934 / 0.9935, ISCX-Tor2016 0.9930 / 0.9872, USTC-TFC2016 0.9962 / 0.9953, MOBILE-APP 0.9893 / 0.9892. Baseline BPF-GNN is higher on USTC-TFC2016 (0.9978 / 0.9967). (Table 2)"
}, url['supclgnn'], "Full text; field locators in each value")
    detail('vfrdad', {
        "Traffic unit definition": "A flow is a sequence of packets sharing an identical five-tuple (source/destination IP, source/destination port, transport protocol), ordered by arrival time; bidirectional sessions are used. (Section 3.1)",
        "Input representation": "Each bidirectional session is mapped to a fixed 784-byte prefix reshaped into a 28×28 single-channel grayscale image. (Section 3.1; Section 4.1)",
        "Packets / bytes": "Fixed 784 bytes per session (truncation for longer, zero-padding for shorter); no header/payload distinction stated. (Section 3.1; Section 4.1)",
        "Preprocessing / anonymisation": "Flow separation by five-tuple, anonymisation by setting source/destination IP addresses to 0 in the byte stream, removal of duplicate and no-payload packet streams, zero-padding/truncation to 784 bytes, conversion to hexadecimal byte stream. (Section 3.1)",
        "Architecture": "Four modules: (1) Multi-scale local feature extraction via Fourier high-pass filtering (D_r ∈ {5,10,15,20}) followed by a 3-layer CNN; (2) Global feature extraction via a traffic-domain autoencoder (3-layer dilated CNN, dilation rate 2, output channels 2) for RGB channel remapping, then a pre-trained ViT; (3) Gated-attention fusion module with 2-layer MLP computing adaptive weights; (4) Classifier. (Section 3.2; Section 3.3; Section 3.4; Fig. 1)",
        "Parameters": "Full VFRDAD model: 92.0M parameters. (Table 15)",
        "Training / evaluation datasets": "Darknet-dataset-2020 (8 classes: Browsing, Chat, Email, Audio Streaming, Video Streaming, File Transfer, P2P, VoIP across Freenet, Tor, I2P, ZeroNet); ISCXVPN2016 (6 categories: Chat, Email, File Transfer, Streaming, P2P, VoIP in VPN and NoVPN subsets); CIC-IoT-2023 (7 attack categories: DDoS, DoS, Recon, Web-based, Brute Force, Spoofing, Mirai). (Section 4.1; Tables 1–3)",
        "Split strategy": "Session-level split: one bidirectional session → one image, no duplication across training/validation/test sets; balancing performed after splitting by randomly selecting up to 3000 samples per category. (Section 4.1)",
        "Metrics": "Accuracy, Precision, Recall, F1 score (weighted harmonic mean); formulas provided. No explicit averaging scheme (macro/weighted/micro) stated. (Section 4.1; Formula (17))",
        "Reported results": "Darknet-Dataset-2020: Freenet 0.9678 Acc / 0.9679 F1, I2P 0.9552 Acc / 0.9556 F1, Tor 0.9669 Acc / 0.9669 F1, ZeroNet 0.9932 Acc / 0.9932 F1; ISCXVPN2016: 0.9955 Acc / 0.9956 F1; CIC-IoT-2023: 0.9926 Acc / 0.9931 F1. (Tables 4–7)",
        "Hardware": "RTX 2080 Ti GPU, Intel Xeon Platinum 8255C CPU @ 2.50 GHz, 64 GB memory. (Section 4.1)",
        "Measurement scope": "Model size (parameters), FLOPs per sample, inference latency, and peak memory usage during inference. Covers the full model pipeline. (Table 15)",
        "Deployment limitations": "Suitable for deployment on network gateways or monitoring servers with moderate compute resources; moderate overhead in parameters, FLOPs, latency, and memory. (Section 4.3.3)",
        "Latency": "Full VFRDAD 13.8 ms per sample (ViT only 11.5 ms), offline. (Table 15)",
        "Memory": "980 MB peak memory for full VFRDAD (ViT only 850 MB). (Table 15)",
        "Pretraining objective": "Traffic-domain autoencoder pretrained self-supervised with MSE on the traffic images; the ViT starts from a pre-trained backbone. (Sections 3.3.1–3.3.2)"
}, url['vfrdad'], "Full text; field locators in each value")
