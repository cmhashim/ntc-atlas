"""Full-text extraction for twelve 2025-2026 method papers, read from corpus/ PDFs on 2026-10-19.
Every value is stated in the PDF at the given locator; unstated values are left out or marked NA.
Fields already set by curator fixes or comparison_review (TrafficFormer pretraining objective,
CATO throughput/latency/scope, Akem hardware/latency/memory/scope) are deliberately not repeated here.
"""
NR='NA — not reported in reviewed sections'

def extract(detail):
    detail('trafficformer',{
        'Traffic unit definition':'Flow (5-tuple) split by SplitCap; pre-training structures traffic as bursts of consecutive same-direction packets.',
        'Input representation':'Hexadecimal packet bytes tokenised as bigrams with BPE; first 5 packets per flow in fine-tuning.',
        'Packets / bytes':'64 bytes per packet after the Ethernet layer; first 5 packets per flow; maximum sequence length 512.',
        'Architecture':'Transformer encoder: 12 layers, 12 attention heads, encoding dimension 768.',
        'Pretraining datasets':'About 20 GB, over 600,000 flows: ISCX-NonVPN (non-VPN portion), CICMalAnal2017 (2017 benign software traffic) and Browser (Table 3).',
        'Training / evaluation datasets':'Six fine-tuning tasks: Cross-Platform Android (197 classes) and iOS (190), CSTNET-TLS 1.3 (120), ISCX-VPN Service (6) and App (11), USTC-TFC (14) (Table 4).',
        'Preprocessing / anonymisation':'Flows under 2 KB or 3 packets and classes under 10 flows removed; at most 500 flows per class. IP, port, TCP timestamps and TLS timestamps/SNI processed with field augmentation to prevent shortcuts.',
        'Split strategy':'Per-class 8:1:1 train/validation/test split of flows.',
        'Metrics':'Accuracy, precision, recall and F1; per-class one-vs-rest values averaged across classes.',
        'Reported results':'TrafficFormer w/ EA F1: Cross-Platform Android 0.6167, iOS 0.4689, CSTNET-TLS 1.3 0.8338, ISCX-VPN Service 0.9580, App 0.7129, USTC-TFC 0.9830 (Tables 5–7).',
        'Hardware':'NVIDIA A100 GPUs; pre-training batch 64 on 3 GPUs (effective 192).',
    },'https://ieeexplore.ieee.org/document/11023272/','Sections 3.2.1, 4.1–4.2; Tables 3–7')

    detail('miett',{
        'Traffic unit definition':'Flow treated as a bag of packet instances.',
        'Input representation':'Hexadecimal packet content tokenised as two-byte bigrams with BPE (dictionary 65,536); per-packet [CLS] token; Netbench-preprocessed data.',
        'Packets / bytes':'5 packets per flow, 128 tokens per packet; pre-training samples 5 of the first 10 packets.',
        'Architecture':'12 Two-Level Attention layers (packet and flow attention), embedding dimension 768; mean-pooled packet [CLS] embeddings feed an MLP.',
        'Pretraining objective':'Masked Flow Prediction (15% masking) plus Packet Relative Position Prediction and Flow Contrastive Learning, weighted sum of the three losses (Eq. 13).',
        'Pretraining datasets':'Unlabelled training sets of the five Netbench datasets used for evaluation.',
        'Training / evaluation datasets':'ISCXVPN 2016 (6 VPN service labels), ISCXTor 2016 (7), CrossPlatform Android (212) and iOS (196), CICIoT 2023 (7 IoT attack labels) (Table 2).',
        'Split strategy':'8:1:1 train/validation/test.',
        'Metrics':'Accuracy and F1; averaging not stated.',
        'Reported results':'Accuracy/F1: ISCXVPN 76.07%/77.86%, ISCXTor 96.60%/82.15%, Android 93.00%/82.36%, iOS 79.63%/75.03%, CICIoT 2023 88.53%/82.48% (Table 1).',
        'Hardware':'Server with two NVIDIA RTX A6000 GPUs.',
        'Version notes':'Full-text values from arXiv v1 (19 December 2024). The main text gives weight 0.2 to PRPP and MFP, the appendix to PRPP and FCL.',
    },'https://arxiv.org/abs/2412.15306v1','Experiment Setup; Tables 1–2; Appendix Implementation Details')

    detail('cato',{
        'Traffic unit definition':'Connection; feature representation = feature set plus packet depth (maximum depth 50 in the evaluation).',
        'Input representation':'Flow statistics from a 67-feature candidate set (Table 4), extracted by a Rust serving pipeline on Retina.',
        'Architecture':'Multi-objective Bayesian optimisation (HyperMapper) plus a Profiler that compiles and measures each pipeline; served models are decision tree, random forest (100 trees) or a three-hidden-layer DNN.',
        'Training / evaluation datasets':'app-class: live campus traffic, 6 web applications plus other, SNI labels; iot-class: UNSW IoT September 2016 traces, 28 device types, about 134K connections; vid-start: YouTube startup delay, 4,287 connections.',
        'Split strategy':'DT/RF tuned by 5-fold nested cross-validation; final Rust model evaluated on a 20% hold-out test set.',
        'Metrics':'F1 (classification) or RMSE (regression) against end-to-end inference latency, zero-loss throughput or pipeline execution time.',
        'Hardware':'Live traffic: dual Xeon Gold 6248R, 384 GB RAM, 100GbE ConnectX-5. Offline datasets: dual Xeon Gold 6154, 384 GB RAM.',
    },'https://arxiv.org/abs/2402.06099v3','Sections 4, 5.1–5.2; Appendices B–D; Table 2')

    detail('flowlet',{
        'Traffic unit definition':'Five-tuple flow segmented into flowlets where the inter-arrival time exceeds an adaptive threshold, the mean of the IATs in a history window.',
        'Input representation':'Field tokenisation of protocol header fields; protocol-layer embedding added to token, position and segment embeddings.',
        'Packets / bytes':'64 bytes from the network layer per packet; first five packets per flow in fine-tuning; 512 input tokens.',
        'Preprocessing / anonymisation':'IP addresses randomised, ports randomised preserving client/server roles, TCP timestamps shifted by a random base; at most 500 samples per class.',
        'Architecture':'BERT-base: 12 encoder layers, 12 heads, dimension 768, about 110M parameters.',
        'Pretraining objective':'Masked Field Model (15% of tokens, half from key header fields) plus Flowlet Prediction Task (ordered, swapped or different-flow pair); losses summed.',
        'Pretraining datasets':'About 30 GB: ISCX-VPN2016 NonVPN, CIC-IDS2017 Monday and WIDE backbone (1 January 2024) (Table 9).',
        'Training / evaluation datasets':'Eight datasets, seven tasks: ISCX-VPN Service and App, ISCX-Tor2016, CSTNET-TLS, Browser, USTC-TFC, CIC-IDS2017, CIC-IoT2022; pre-training and fine-tuning data stated as strictly separated.',
        'Split strategy':'8:1:1 train/validation/test; Appendix E repeats the malware task over five random seeds.',
        'Metrics':'Accuracy; macro-averaged precision, recall and F1.',
        'Reported results':'F1: ISCX-VPN Service 0.9364, ISCX-Tor 0.9116, ISCX-VPN App 0.7712, CSTNET-TLS 0.8473, Browser 0.6684, USTC-TFC 0.9648, CIC-IDS2017 0.9079, CIC-IoT2022 0.8859 (Tables 2–3).',
        'Throughput':'150.04 samples/s inference on one GPU (Table 6).',
        'Memory':'28 GB GPU memory in pre-training (6 GPUs), 17 GB in fine-tuning (1 GPU) (Table 6).',
        'Hardware':'Server with 8 NVIDIA Tesla V100S GPUs.',
        'Measurement scope':'Offline model inference rate on one GPU; not a live-traffic throughput.',
        'Version notes':'Full-text values from arXiv v1 (27 August 2025).',
    },'https://arxiv.org/abs/2508.19924v1','Method; Experiment Setup; Tables 2–3, 6, 9; Appendix D')

    detail('akem',{
        'Traffic unit definition':'5-tuple flow; in-switch inference triggers after the first n packets (n = 4 or 8 performed best).',
        'Input representation':'Packet size and inter-arrival time; in-switch features are max, min, total and mean of both plus current packet size. Ports and other header fields excluded.',
        'Architecture':'Random forest mapped to Tofino match-action tables with the Planter scheme (depth 16–20, 1–5 trees, 4–5 features retained).',
        'Training / evaluation datasets':'NIMS IMA (6 instant-messaging apps), Netflow QUIC (5 Google services), ISCXVPN2016 (7 classes incl. BROWSING labelled by ports 80/443) (Table 2).',
        'Split strategy':'12-fold cross-validation; stratified folds in the offline analysis.',
        'Metrics':'Macro, weighted and micro F1; macro is the unweighted mean of per-class F1.',
        'Reported results':'In-switch macro F1: ISCX VPN 85.65%, NIMS IMA 90.29%, Netflow QUIC 90.30%; weighted F1 87.14%, 89.82%, 95.29% (Figure 6).',
        'Throughput':'More than 100 Gbps aggregate through the switch (DPDK-PktGen background plus replayed pcaps); the classified encrypted traffic ran at Kbps to Mbps levels.',
    },'https://dspace.networks.imdea.org/handle/20.500.12761/1878','Sections 3.1–3.3, 4.1–4.2, 5.1–5.2, 6.1; Table 2; Figure 6')

    detail('mhnet',{
        'Traffic unit definition':'Bidirectional flow (SplitCap), at most the first 15 packets; ISCX-Tor flows divided into 60-second blocks.',
        'Input representation':'4-bit and 8-bit traffic units per packet form multi-view heterogeneous graphs with header-header, payload-payload and header-payload PMI edges.',
        'Preprocessing / anonymisation':'Ethernet header, IP addresses and ports removed; flows without payload or longer than 10,000 filtered.',
        'Architecture':'4-layer heterogeneous GraphSAGE encoder per packet, LSTM over packets for the flow representation.',
        'Fine-tuning objective':'End-to-end multi-task loss: packet and flow classification plus packet- and flow-level contrastive losses (Eq. 12); no separate pre-training.',
        'Training / evaluation datasets':'CIC-IoT 2022 (6 classes), ISCX-VPN (6), ISCX-NonVPN (6), ISCX-Tor (8), ISCX-NonTor (8), each run independently (Appendix Table 4); CrossPlatform Android in the appendix.',
        'Split strategy':'Stratified 9:1 flow-level train/test; packet-level sets inherit the flow split.',
        'Metrics':'Overall accuracy and macro F1; mean over five runs.',
        'Reported results':'Flow-level accuracy/macro F1: CIC-IoT 0.9900/0.9896, ISCX-Tor 0.9886/0.9886, ISCX-NonTor 0.9465/0.9453, ISCX-VPN 0.9942/0.9941, ISCX-NonVPN 0.9141/0.9141 (Table 1).',
        'Hardware':'One NVIDIA RTX 3080.',
    },'https://arxiv.org/abs/2501.03279v1','Method; Experimental Settings; Tables 1–2; Appendix More Experimental Details, Table 4')

    detail('fastflow',{
        'Input representation':'Packet sequence (direction, payload size in MTU units, log inter-arrival time) and slot sequence of per-time-interval aggregates.',
        'Architecture':'Two LSTM classifiers (packet and slot) making sequential decisions, trained with reinforcement learning; augmentation creates pseudo-unknown flows.',
        'Training / evaluation datasets':'Lab: UTMobileNet, VNAT, UNIBS (Table 2). Deployment: about 1 million campus flows labelled by a commercial classifier for training; 22.9 million live flows, 7 application types, 32 providers (Table 5).',
        'Split strategy':'Lab: random 70/30 train/test over ten iterations; about 20–25% of flows (some flow types) held out as unknown; packet drops injected only into test data.',
        'Metrics':'Macro F1, accuracy, packets and time to classify, unknown-type FPR and TPR.',
        'Reported results':'Lab macro F1 under disorder and unknown types: UTMobileNet 85.42%, VNAT 96.24%, UNIBS 92.30% (Table 3). Campus application types: macro F1 90.23%, accuracy 91.45% (Table 6).',
        'Throughput':'About 30K concurrent flows per time-series classifier on one Xeon E5-2620 core; up to 200K concurrent flows for both classifiers on an RTX 4090 (benchmarked, not deployed).',
        'Hardware':'Deployment server: 8-core Intel Xeon E5-2620, 64 GB RAM, two 10 Gbps interfaces; training on one NVIDIA RTX 4090 (about 6 hours).',
    },'https://doi.org/10.1145/3727115','Sections 4.1–4.2, 6.1–6.2, 6.4; Tables 2–3, 5–7')

    detail('etool',{
        'Traffic unit definition':'Multiple flows of a client grouped by flow-level BURST (start-time threshold 1 s) into a traffic relation graph; each flow is a node.',
        'Input representation':'Per flow: 128 datagram bytes as two-byte units plus a directed packet-size sequence.',
        'Architecture':'Vicuna-7B-v1.5 LLM (32 decoder layers) with a flow-graph encoder and structure-aware projector; LLM and graph encoder frozen during instruction tuning.',
        'Pretraining objective':'Graph structural instruction tuning: traffic graph encoding alignment and self-supervised BURST graph matching, followed by traffic-task instruction tuning.',
        'Training / evaluation datasets':'APP53-TIME (28 classes) and APP53-VERSION (25) for I.I.D. and time/version-shift tasks, ISCX-Botnet (binary and 8-class type shift), NETD built from ISCX-VPN (Table II).',
        'Split strategy':'Shift tasks fine-tune on one time or version and test zero-shot on another; NETD uses 1:3 and 3:1 component ratios and an 80% application subset. Split ratios NA — not reported in reviewed sections.',
        'Metrics':'Accuracy; macro-averaged precision, recall and F1.',
        'Reported results':'F1: APP53-TIME 93.19%, APP53-VERSION 92.11%, APP53 ⇒ TIME 74.88%, APP53 ⇒ VERSION 72.13% (Table IV).',
        'Parameters':'131,612,672 tuned parameters with the LLM frozen; 6,607,884,288 with LLM tuning, which ran out of memory (Table VII).',
        'Memory':'71,196 MB single-GPU memory for frozen traffic-task tuning (Table VII).',
        'Latency':'3,756.62 ms per response on NETD with one NVIDIA A800 (Table VII).',
        'Hardware':'NVIDIA Tesla A800 80 GB GPUs; efficiency study on two A800s.',
        'Deployment limitations':'The authors state ETooL does not yet meet real-time detection requirements.',
    },'https://doi.org/10.1109/TIFS.2025.3574971','Sections V-A, VI, VIII-A, VIII-B, VIII-E; Tables II, IV, VII')

    detail('mm4flow',{
        'Traffic unit definition':'Bidirectional flow; flows with fewer than 5 payload-carrying packets discarded.',
        'Input representation':'Two modalities: first 256 transport-payload bytes per direction (512 bytes, headers excluded) and the signed payload-length sequence of packets with payload.',
        'Architecture':'BERT-bytes and BERT-ps (BERT-base settings, 12 layers, hidden 768) fused by cross-attention for fine-tuning; 174.40M parameters (Table 1).',
        'Pretraining objective':'Masked language modelling (15% of tokens) on each modality separately.',
        'Pretraining datasets':'About 77.6 TB pcap from a network gateway over one week; 465M flows; stated to exclude downstream evaluation data.',
        'Training / evaluation datasets':'DataCon2020, DataCon2021-p1, DataCon2021-p2, Browser, NUDT_MobileTraffic, CSTNET-TLS1.3 (Table 5).',
        'Split strategy':'Fixed per-class sample count for a balanced training set, split 9:1 train/validation; remaining samples form the test set, downsampled for large classes.',
        'Metrics':'Accuracy; macro-averaged precision, recall and F1.',
        'Reported results':'Accuracy: DataCon2020 0.9734, DataCon2021-p1 0.9731, DataCon2021-p2 0.9011, Browser 0.9929, NUDT_MobileTraffic 0.9111, CSTNET-TLS1.3 0.9826 (Table 2).',
        'Hardware':'AMD EPYC 7542, 8 NVIDIA RTX 6000 Ada, 512 GB RAM; pre-training on 4 GPUs for about 350 hours.',
    },'https://doi.org/10.1145/3719027.3744804','Sections 3.2–3.5, 4.1–4.2; Tables 1–2, 4–5; Appendix C')

    detail('unflows',{
        'Input representation':'76 CICFlowMeter flow features, z-score normalised.',
        'Architecture':'Fully connected autoencoder with re-input structure (76-32-16-4 encoder, symmetric decoder), trained on benign flows; flow spectrum plus k-means behaviour detector.',
        'Training / evaluation datasets':'NSL-KDD, UNSW-NB15, Kitsune, CIC-IDS-2017, CSE-CIC-IDS-2018, CIC-DDoS-2019.',
        'Split strategy':'CIC-IDS-2017: trained on Monday benign traffic, tested on Tuesday to Friday. Splits for the other datasets NA — not reported in reviewed sections.',
        'Metrics':'AUC, FPR, FNR and per-attack recall.',
        'Reported results':'CIC-IDS-2017 flow-based detection: average AUC 0.9235 (Table IV); AUC above 0.975 on NSL-KDD, UNSW-NB15 and CIC-DDoS-2019.',
        'Latency':'0.0161 s per 10,000 flows for unFlowS-Net detection (Fig. 8).',
        'Hardware':'Intel Core i9-10900K, NVIDIA RTX 3090, 128 GB RAM.',
        'Measurement scope':'Batch processing time for 10,000 flows; whether feature extraction is included is not stated.',
    },'https://doi.org/10.1109/TIFS.2025.3550060','Sections IV-A, IV-B, V-A–V-C, VI-A, VI-D; Tables II, IV; Fig. 8')

    detail('semiaf',{
        'Traffic unit definition':'Traffic segment of multiple flows within a time window, each flow split into in-flow bursts.',
        'Input representation':'Packet-length and timing sequences per in-flow burst, embedded by a GRU; bursts are nodes of an in-flow burst interaction (IFBI) graph.',
        'Architecture':'Graph attention network with contrastive learning: node classification for in-app actions, graph classification for app names; GNNExplainer interpreter.',
        'Training / evaluation datasets':'FOAP (1,000 apps, app and action labels), FG-Net D1/D2 (53 apps, captured one month apart), NUDT MobileTraffic (100 apps, 1,336,007 flows) (Table I).',
        'Evaluation setting':'Unknown apps: FOAP split into known and unknown subsets of 500 apps each; trained on known apps, unknown embeddings clustered.',
        'Split strategy':'Train/test ratio for known-app identification NA — not reported in reviewed sections.',
        'Metrics':'Precision, recall, F1 (averaging not stated); Rand, Fowlkes-Mallows, homogeneity, completeness and V-measure for clustering.',
        'Reported results':'F1: FOAP app 0.992, FOAP action 0.865, FG-Net D1 0.961, D2 0.925, NUDT MobileTraffic 0.921 (Table II).',
        'Latency':'Per flow: 5.42 ms for app identification (3.36 preprocessing, 2.06 prediction), 20.9 ms for action identification (Table V).',
        'Throughput':'Authors calculate operation at 133 Mbps while keeping 80% accuracy; a calculated figure, not a measured live rate.',
        'Hardware':'Intel i9-13900KF, 64 GB RAM, one NVIDIA RTX 4090.',
    },'https://doi.org/10.1109/DSN64029.2025.00051','Sections IV, V-A–V-C, V-E; Tables I–II, V–VI')

    detail('robustnessmatters',{
        'Traffic unit definition':'Bidirectional 5-tuple flow; packets without transport payload ignored; flows with fewer than 5 payload packets discarded.',
        'Input representation':'Signed transport-payload length sequence; vocabulary of lengths 1–1500 in two directions plus 5 special tokens.',
        'Architecture':'BERT-ps: bidirectional Transformer encoder with BERT-base settings and a fully connected classification head.',
        'Pretraining objective':'Masked language modelling, 15% of tokens (80% [MASK], 10% random, 10% unchanged).',
        'Pretraining datasets':'About 12.1 TB pcap from a network gateway over one week; 76.11M packet-length sequences (about 2.96B tokens).',
        'Training / evaluation datasets':'DataCon2020, DataCon2021-p1 (6 proxies), DataCon2021-p2 (22 websites), EBSNN-dataset (22 categories), CSTNET-TLS1.3 (80 applications).',
        'Evaluation setting':'Robustness compared on DataCon2020 against packet-length baselines under packet loss, retransmission and disorder, using PA-curve and PA-area.',
        'Metrics':'Accuracy and macro-F1; PA-curve and PA-area for robustness.',
        'Reported results':'BERT-ps accuracy about 90% on DataCon2021-p2 and 97.5% on CSTNET-TLS1.3.',
        'Latency':'About 0.59 s per 1,000 flows; feature extraction about 0.07 s per 1,000 flows, 12% of the total (Table VI).',
        'Hardware':'AMD EPYC 7542, 8 NVIDIA RTX 6000 Ada, 512 GB RAM.',
    },'https://doi.org/10.1109/TIFS.2025.3613970','Sections IV, V-A–V-C, VI-A–VI-C; Table VI; Appendix B')
