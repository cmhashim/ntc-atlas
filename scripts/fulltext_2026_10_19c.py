"""Task 22 (2026-10-19): full-text extraction for 12 abstract-only papers (2024–2025).
Same pipeline as Task 21: one model per paper (MODEL), verbatim quote per value, Claude checked quotes and
numbers against corpus/ PDFs. Fields already tied to a full-text or curator record are not overwritten."""

MODEL = {
 "sugar": "Codex",
 "demystifying": "Codex",
 "onetask": "Codex",
 "simple": "GLM",
 "netbench": "GLM",
 "cletfe": "GLM",
 "lens": "Gemini",
 "trafficgpt": "Gemini",
 "platforms": "Gemini",
 "iisy": "Mistral",
 "leo": "Mistral",
 "cruisecontrol": "Mistral"
}

# Catalogued collections each paper names in its full text, with that paper's own locator.
DATASETS = {
 "demystifying": [
  [
   "crossplatform"
  ],
  "Section 4.2; Table 1"
 ],
 "simple": [
  [
   "iscxvpn",
   "mirage19",
   "mirage22",
   "utmobile",
   "ucdavis",
   "cicids2017"
  ],
  "Section 3.3; Table 1"
 ],
 "netbench": [
  [
   "iscxvpn",
   "iscxtor",
   "ustc",
   "crossplatform"
  ],
  "Table 1"
 ],
 "cletfe": [
  [
   "iscxvpn",
   "iscxtor"
  ],
  "Section 4.1.1"
 ],
 "lens": [
  [
   "iscxvpn",
   "iscxtor",
   "ustc",
   "crossplatform"
  ],
  "Section 4.1; Appendix A.3, Table 11"
 ],
 "trafficgpt": [
  [
   "crossplatform",
   "iscxvpn",
   "ustc"
  ],
  "Section IV-B"
 ],
 "leo": [
  [
   "cicids2017"
  ],
  "Section 7.2"
 ],
 "cruisecontrol": [
  [
   "caida"
  ],
  "Section 5"
 ]
}


def extract(detail, P, D=()):
    url = {p["id"]: p["url"] for p in P}
    for p in P:
        if p["id"] in DATASETS:
            p["datasets"] = list(dict.fromkeys(p["datasets"] + DATASETS[p["id"]][0]))
    for d in D:
        d["papers"] = [p["id"] for p in P if d["id"] in p["datasets"]]
    detail('cletfe', {
        "Traffic unit definition": "Dual packet-level and flow-level classification; samples are bidirectional flows capped at 15 packets, with ISCX-Tor flows additionally divided into 60-second non-overlapping blocks. (Section 4.1.2; Section 4.1.3)",
        "Input representation": "Byte-level traffic graphs (TFE-GNN style) where nodes are byte values and edges encode semantic correlation between bytes; packet vectors are fused into a flow embedding by an LSTM. (Section 3.2.1; Section 3.2.2)",
        "Packets / bytes": "At most the first 15 packets of a flow are used; packet bytes (after Ethernet/IP/port removal) form the byte-level traffic graph, with header and payload graphs perturbed separately in ablations. (Section 4.1.2; Table 3)",
        "Preprocessing / anonymisation": "SplitCap extracts bidirectional flows; ISCX-Tor flows are enriched by 60-second non-overlapping blocks; flows without payload or surpassing length 10000 are filtered; bad and retransmission packets removed; Ethernet header, IP addresses and port numbers removed. (Section 4.1.2)",
        "Architecture": "A shared TFE-GNN graph encoder produces packet vectors, an LSTM fuses them into flow vectors, and PReLU MLP heads classify both levels; views are augmented by node, edge and packet dropping (ratios 0.05, 0.1, 0.6) with temperature 0.07. Two modules: dual-level contrastive learning and cross-level multi-task learning. (Section 3.1; Section 3.4; Section 4.1.3)",
        "Parameters": "No absolute parameter count is stated; Figure 3(b) (in millions) shows CLE-TFE's parameters only slightly above TFE-GNN due to the added packet-level classification head, and far below ET-BERT. (Section 4.5; Figure 3(b))",
        "Fine-tuning objective": "End-to-end joint objective in a single training (no pretraining): L = L_PCLS + L_FCLS + alpha*L_PCL + beta*L_FCL, combining cross-entropy classification losses at packet and flow levels with supervised contrastive losses weighted by alpha, beta in [0,1]. (Section 3.4)",
        "Training / evaluation datasets": "ISCX VPN-nonVPN (ISCX-VPN and ISCX-nonVPN) divided into six categories and ISCX Tor-nonTor (ISCX-Tor and ISCX-nonTor) into eight; all experiments run independently on the four datasets, with statistics in Appendix E. (Section 4.1.1)",
        "Split strategy": "Flow-level stratified sampling into 9:1 train:test by number of traffic flows for all datasets; packets of the flow-level train/test sets serve directly as packet-level train/test, inheriting their flow's label. (Section 4.1.2)",
        "Metrics": "Overall Accuracy (AC), Precision (PR), Recall (RC) and Macro F1-score (F1); averaging for PR/RC is not stated. (Section 4.1.3)",
        "Hardware": "NVIDIA RTX 3080 GPU, implemented in PyTorch and Deep Graph Library; results are means over five runs. (Section 4.1.3)",
        "FLOPs": "About 1/14 of ET-BERT's FLOPs; smaller than TFE-GNN because a shorter flow length suffices, with augmentation and contrastive loss adding negligible extra cost. (Abstract; Section 4.5)",
        "Measurement scope": "Efficiency numbers cover only FLOPs and parameter counts (offline comparison with ET-BERT, TFE-GNN and CLE-TFE w/o AUG&CL); no throughput, latency or memory measurements are reported. (Section 4.5)",
        "Deployment limitations": "The graph augmentation is non-trainable and may give sub-optimal results; hard negative samples are not optimised sufficiently; jointly optimising both tasks in one training introduces trade-offs between the two tasks. (Section 6; Section 4.2)",
        "Leakage / shortcut risks": "The authors remove IP addresses and port numbers to eliminate potential interference such fields could otherwise introduce; no other leakage or shortcut tests are reported. (Section 4.1.2)"
}, url['cletfe'], "Full text; field locators in each value")
    detail('cruisecontrol', {
        "Traffic unit definition": "Flow-level processing with per-flow state; early detection tasks use first 10 packets per connection. (Section 2.1; Section 3.2; Section 4.2)",
        "Input representation": "Network flow metrics, transport layer indicators, application-layer traffic pattern features, and raw IP/TCP headers. (Section 4.2)",
        "Packets / bytes": "Service recognition uses first 10 packets per flow; video quality uses continuous feature extraction; CAIDA trace at 1.1 MPPS. (Section 2.3; Section 4.2; Section 5)",
        "Preprocessing / anonymisation": "Header parsing, packet filtering, flow tracking, data reassembly; CAIDA Anonymized Internet Traces 2016 used. (Section 2.1; Section 3.2; Section 5)",
        "Architecture": "Workers for feature extraction, Post-Processor for aggregation, Monitor for packet loss detection, Model Selection module; Rust with DPDK and Retina v0.1. (Section 3; Section 4.1)",
        "Training / evaluation datasets": "Bronzino et al. [12] video quality dataset for training; CAIDA Anonymized Internet Traces 2016 (20160121) from Equinix Chicago for evaluation. (Section 4.2; Section 5)",
        "Metrics": "Median Absolute Error (MAE) in ms for video quality; packet loss percentage; median accuracy. (Table 1; Section 5)",
        "Reported results": "Cruise Control improves median task accuracy by 2.78% and reduces packet loss by a factor of four versus static models; video quality: 0.37% loss with m3 median accuracy; service recognition: 0.117% vs 0.343% loss for static m3. (Abstract; Section 5.1; Tables 4-5)",
        "Hardware": "Dual 16-core AMD EPYC 7343 CPUs, 100GbE Intel E810 NIC, 384GiB DDR4 per server; servers connected via 100GbE switch; TRex traffic generator. (Section 5)",
        "Throughput": "10 Gbps average with 1.1 MPPS for CAIDA trace; up to 3 Mcps (million connections/second) with 8 workers in worst-case new connection scenario. (Section 5; Table 6)",
        "Memory": "384GiB DDR4 per server; thread-local hashmaps can cause memory exhaustion with many workers or long export windows. (Section 5; Section 5.3)",
        "Measurement scope": "Packet loss rates, feature extraction throughput, and model accuracy; covers feature computation and export pipeline but not ML inference. (Section 5; Section 5.1)",
        "Deployment limitations": "Feature export halts traffic processing for several seconds; thread-local hashmaps risk memory exhaustion; AMD CPUs preclude Intel DDIO; requires careful parameter calibration. (Section 3.2; Section 5; Section 5.3)",
        "Evaluation setting": "Compared against Retina and CATO static configurations using TRex-generated CAIDA traffic; single Worker core except for multi-core scalability tests. (Section 5; Section 5.1)"
}, url['cruisecontrol'], "Full text; field locators in each value")
    detail('demystifying', {
        "Traffic unit definition": "The intrinsic evaluation operates on flow embeddings extracted from each model's final encoder layer. (Section 3.1, Methodology)",
        "Input representation": "The framework analyses frozen encoder embeddings and compares them with CICFlowMeter features; causal tests additionally use embeddings from perturbed traffic. (Sections 3.2 and 3.3; Figure 1)",
        "Preprocessing / anonymisation": "Datasets are processed into flow records using the original models' data processing scripts, preserving their original input pipelines. Protocol perturbations modify semantically meaningful packet features rather than applying identical token changes across models. (Sections 4.1, 4.2 and 4.5)",
        "Fine-tuning objective": "A linear classifier is trained on frozen raw or normalised embeddings for downstream classification; logistic regression probes distinguish synthetic network contexts. (Sections 3.3 and 4.3; Appendix D)",
        "Training / evaluation datasets": "Evaluation uses Android Crossmarket, CIC-IDS2017, CIC-APT-IIoT24, CAIDA and MAWI. NetReplica additionally generates synthetic contexts varying congestion control, active queue management and cross-traffic. (Sections 4.2 and 4.6; Table 1; Appendices B and J)",
        "Metrics": "Intrinsic metrics include mean pairwise cosine similarity, Mean Cosine Contribution and Centered Kernel Alignment with CICFlowMeter features. Additional analyses report F1 and F1 gain, intrinsic dimension, silhouette score and L1 distance. (Sections 3.1–3.3 and 4.3; Appendices F–H)",
        "Reported results": "The authors' decorrelation intervention improves NetMamba F1 by 0.35 ± 0.02 on Crossmarket, 0.11 ± 0.27 on CIC-IDS2017 and 0.03 ± 0.02 on CIC-APT-IIoT24. These gains use a single linear layer trained for 30 epochs over five runs. (Section 4.3; Table 2)",
        "Hardware": "All experiments run on a single node with 4 A100 GPUs, each with 80 GB GPU RAM, and 512 GB host RAM. (Appendix I)",
        "Deployment limitations": "The evaluated models depend on payload information that may be encrypted or absent in production, creating a robustness concern. Metric alignment is also weaker on real-world traffic than on controlled datasets. (Sections 4.4 and 4.5)",
        "Evaluation setting": "Unmodified public pretrained checkpoints of YaTC, ET-BERT, netFound and NetMamba are evaluated through frozen embedding geometry, alignment with expert features and causal sensitivity tests. Tests include protocol-feature perturbations and linear probing of synthetic network contexts. (Sections 3, 4.1, 4.5 and 4.6)",
        "Leakage / shortcut risks": "The authors identify dataset-specific shortcuts as a weakness of downstream-only evaluation. Their perturbation tests expose payload dependence and selective sensitivity to sequence/acknowledgement numbers, while their limitations acknowledge potentially flawed or biased public datasets. (Sections 2.3, 4.5 and 5)"
}, url['demystifying'], "Full text; field locators in each value")
    detail('iisy', {
        "Traffic unit definition": "Packet, flow, aggregate, and file granularity. (Section I)",
        "Input representation": "Packet header fields, flow state metrics, aggregate traffic features, and file payload data extracted from csv or pcap inputs. (Section IV; Section VI)",
        "Preprocessing / anonymisation": "Feature selection by ML importance score; Jane Street features anonymized; quantization and normalization for fixed-point encoding. (Section VI; Section VIII-A2; Section V-C)",
        "Architecture": "Match-Action pipeline on RMT/PISA-based programmable switches (Intel Tofino, NetFPGA SUME). (Section V)",
        "Parameters": "DT/RF: up to 59 numerical or 30 ASCII features; XGBoost: up to 55 numerical or 30 ASCII; max 20 trees with depth up to 15. (Section VIII-D)",
        "Training / evaluation datasets": "UNSW-NB15 (network anomaly detection), Jane Street Market Prediction (financial transactions), Iris (flower classification). (Section VIII-A; Section VIII-C)",
        "Split strategy": "80% training, 20% testing. (Section VIII-A1; Section VIII-A2)",
        "Metrics": "Misclassification rate, F1 score, accuracy, error rate. (Section VIII-G)",
        "Reported results": "Backend load reduced by 70%; baseline F1=0.9888 with 0.49% misclassification; at 0.7 confidence switch handles 84.5% traffic with F1=0.976. (Abstract; Section VIII-G)",
        "Hardware": "Intel Barefoot Tofino ASIC (64×100G ports), NetFPGA-SUME FPGA. (Section VII)",
        "Throughput": "Line rate 6.4Tbps; 25× to 80,000× improvement over CPU classification. (Abstract; Section VIII-F)",
        "Latency": "Sub-microsecond classification; ×10² to ×10³ better than CPU. (Abstract; Section VIII-F)",
        "Memory": "DT/RF <1.9% memory; all models <9.3%; classical models <6.7%. (Section VIII-C)",
        "Measurement scope": "Throughput and latency measured using pcap traces and UDP packets; compared to layer 2 forwarding and CPU. (Section VIII-F)",
        "Deployment limitations": "Constrained switch resources limit model size and accuracy; limited by tables, stages, PHV bit-width. (Section II-C)",
        "Evaluation setting": "Evaluation of DT, RF, XGBoost, SVM, K-means, Naïve Bayes on Tofino for anomaly detection and finance using pcap traces. (Section VIII)"
}, url['iisy'], "Full text; field locators in each value")
    detail('lens', {
        "Traffic unit definition": "Flow-level traffic segmented with SplitCap by the standard 5-tuple, using the first 34 packets for classification, and packet-level traffic (one packet sampled per flow) for generation. (Section 4; Appendix A.1)",
        "Input representation": "Text-like sequences parsed via Tshark including network, transport, and application metadata followed by a 12-byte hexadecimal payload, tokenised using a Byte-level Byte Pair Encoding tokenizer alongside task context. (Section 3.1; Appendix A.1)",
        "Packets / bytes": "Classification uses the first 34 packets per flow (up to a 1,500 token limit), appending a 12-byte hexadecimal application payload per packet. (Appendix A.1)",
        "Preprocessing / anonymisation": "Flows are extracted using SplitCap, parsed with Tshark, and all source and destination IP addresses are replaced with placeholder tokens (<SIP> and <DIP>). (Appendix A.1)",
        "Architecture": "T5-v1.1-base encoder-decoder architecture implemented via TurboT5, comprising 12 encoder layers, 12 decoder layers, 12 attention heads of dimension 64, hidden dimension 768, MLP hidden dimension 2048, and Gated-GeLU activation. (Section 4; Appendix E, Table 17)",
        "Parameters": "Roughly 0.25 billion parameters. (Section 4)",
        "Pretraining objective": "Knowledge-Guided Masked Span Prediction (KG-MSP) which masks metadata and payload fields based on network importance, combined with natural language context span masking at an overall 15% mask ratio. (Section 3.2; Section 3.2.1)",
        "Pretraining datasets": "A 60% stratified flow sample from ISCX-VPN, ISCX-Tor, USTC-TFC-2016, CIC-DoHBrw-2020, and CIC-IoT-2023, coupled with the mini C4 natural language corpus for tokenizer training. (Section 4; Appendix A.2, Table 10)",
        "Fine-tuning objective": "Closed-ended text generation using context-aware finetuning, with decoding output space constrained to valid label candidates via a prefix trie. (Section 3.3)",
        "Training / evaluation datasets": "Six datasets comprising 12 classification tasks: ISCX-VPN (tasks 1 to 3; 2, 6, 16 classes), ISCX-Tor / USTC-TFC-2016 (tasks 4 and 5; 7 and 16 classes), Cross Platform Android (tasks 6 and 7; 209 and 3 classes), Cross Platform iOS (tasks 8 and 9; 196 and 3 classes), CIC-DoHBrw-2020 (task 10; 5 classes), and CIC-IoT-2023 (tasks 11 and 12; 2 and 7 classes). (Section 4.1; Appendix A.3, Table 11)",
        "Split strategy": "Stratified sampling of 60% of flows for pretraining on coarse categories; finetuning randomly selects roughly 10k flows per dataset (or 15% for Cross Platform Android and 26% for Cross Platform iOS). (Section 4; Appendix A.2, Table 10)",
        "Metrics": "Accuracy and Macro F1 score for classification; Jensen-Shannon Divergence and Total Variation Distance for generation. (Section 4)",
        "Reported results": "Lens achieved an average accuracy of 96.33% across all 12 classification tasks, reaching 0.9942 accuracy / 0.9870 macro F1 on Task 1, 0.8979 / 0.8893 on Task 2, 0.8406 / 0.8137 on Task 3, 0.9692 / 0.8120 on Task 4, 0.9538 / 0.9676 on Task 5, 0.9660 / 0.8847 on Task 6, 0.9960 / 0.9898 on Task 7, 0.9752 / 0.9492 on Task 8, 0.9951 / 0.9951 on Task 9, 0.9963 / 0.9610 on Task 10, 0.9877 / 0.9870 on Task 11, and 0.9878 / 0.6802 on Task 12. (Section 4.1, Table 2 and Table 3)",
        "Hardware": "A GPU server configured with four NVIDIA A6000 48 GB GPUs running Ubuntu 20.04.6. (Section 4)",
        "Leakage / shortcut risks": "Pretraining stratification uses coarse dataset-level categories without downstream application labels to prevent label leakage, and IP addresses are masked to avert identifier leakage. (Section 4; Appendix A.1)",
        "Version notes": "First posted February 2024; latest reviewed revision January 2026 changes title and byline. The abstract gives 96.33% average accuracy over the 12 tasks; the introduction gives 96.31%. (Abstract; Section 1)"
}, url['lens'], "Full text; field locators in each value")
    detail('leo', {
        "Traffic unit definition": "packet-level classification at line rate. (Abstract)",
        "Input representation": "stateless features from packet header vector and stateful features from switch registers. (§4.3)",
        "Packets / bytes": "per-packet classification; one packet per sample; behavioral flow statistics only, no payload inspection. (§2; §7.4)",
        "Parameters": "decision trees with depth up to 22 and 1024 leaves with TCAM, depth 10 with SRAM; sub-tree multiplexing unit k typically 3. (§5; §7.1)",
        "Training / evaluation datasets": "CICIDS-2017 with 7 classes using 42 switch-compatible features; UNSW-NB15 binary classification using 22 switch-compatible features. (§7.2)",
        "Split strategy": "75:25 train/test split by sample count. (§7.2)",
        "Metrics": "average per-class F1 score macro-averaged. (§7.2)",
        "Reported results": "CICIDS-2017: 0.94 F1 with SRAM, 0.98 F1 with TCAM; UNSW-NB15: 0.92 F1 with SRAM, matches control plane with TCAM; all macro-averaged F1. (§7.2; Figure 12)",
        "Deployment limitations": "resource-constrained by ALU, memory and ~10 pipeline stages; sub-tree multiplexing doubles resource requirements; header field container groups limit k and feature count. (§1; §4.5; §5)",
        "Evaluation setting": "compared against pFor/SwTree-NT, IIsy-NT, Leo-NT and Control Plane baselines on decision tree classification accuracy. (§7.1)"
}, url['leo'], "Full text; field locators in each value")
    detail('netbench', {
        "Traffic unit definition": "Both flows and single packets are used; flows are extracted as packets sharing distinct combinations of IP addresses, port numbers and protocols, and every dataset is offered at both flow level and packet level. (Section 3.1 (Data Pre-Processing, Data Segmentation))",
        "Input representation": "Anonymised packets (header and payload) are converted to hexadecimal, then the WordPiece algorithm segments the hex into 4-digit blocks with symbols </s>, <head> and <pkt> marking sequence ends, header separation and packet demarcation; flow-level input concatenates packets with these markers. (Section 3.1 (Data Standardization); Figure 2)",
        "Preprocessing / anonymisation": "PCAP files are first segmented into distinct training, validation and testing sets before flow extraction, and each packet is anonymised by masking source and destination IP addresses and port numbers, replaced with 0. (Section 3.1 (Data Pre-Processing))",
        "Training / evaluation datasets": "Seven public datasets: ISCXVPN 2016, ISCXTor 2016, USTC-TFC 2016, Cross-Platform (Android) 2020, Cross-Platform (iOS) 2020, CIRA-CIC-DoHBrw 2020 and CIC IoT Dataset 2023, yielding 15 classification tasks with 2 to 212 labels and 5 generation tasks over consecutive packets from the same datasets; totals are 2,952,302 flows and 69,799,192 packets. (Abstract; Table 1)",
        "Split strategy": "Training, validation and testing split at a ratio of 8:1:1; PCAP files are segmented into distinct sets before flows and packets are extracted, so highly correlated same-flow packets cannot appear in both training and testing data. (Section 4.1 (Dataset); Section 3.1 (Data Pre-Processing))",
        "Metrics": "Classification tasks are scored with Accuracy and Macro F1 Score; generation tasks are scored with Jensen-Shannon Divergence and Total Variation Distance. (Section 4.1 (Evaluation metrics))",
        "Reported results": "The benchmark's headline finding is that foundation models ET-BERT and YaTC significantly outperform the traditional deep learning classifiers across the classification tasks (YaTC packet-level reaches 0.9984 accuracy and 0.9961 F1 on Task 1), while traditional methods bias towards dominant classes; NetShare generates IP addresses and port numbers better, STAN generates packet length better. (Section 4.2; Tables 3-5)",
        "Evaluation setting": "Eight major SOTA open-source models are assessed: classifiers DataNet, FS-Net, BiLSTM_ATTN, DeepPacket, TSCRNN, ET-BERT and YaTC, plus generative models STAN and NetShare; ET-BERT and YaTC use released pre-trained weights fine-tuned on the entire prepared training set, FS-Net is evaluated at flow level only, other classifiers at both levels, and generative models use randomly sampled consecutive packets. (Section 4.1 (SOTA Models))",
        "Leakage / shortcut risks": "The authors report that randomly splitting packets of the same flow across training and testing causes data leakage because same-flow packets are strongly correlated, and they flag ET-BERT and YaTC's packet-level processing as facing this risk; NetBench avoids it by splitting PCAPs before extraction. (Section 1; Section 2; Section 3.1)",
        "Deployment limitations": "The authors state that foundation models' input length constraints cause over-long input flows to be truncated, keeping flow-level foundation models from surpassing packet-level ones on some tasks; they add that longer input length is needed for increasingly complex traffic and that very few foundation models investigate traffic generation. (Section 4.2; Section 5 (Conclusion))",
        "Version notes": "Model counts are internally inconsistent: the abstract says eight SOTA classification models plus two generative models, while Section 4.1 counts 8 major SOTA open-source models yet lists seven classification models and two generative models. (Abstract; Section 4.1)"
}, url['netbench'], "Full text; field locators in each value")
    detail('onetask', {
        "Traffic unit definition": "The principal transfer task classifies bidirectional flows, allowing source and destination endpoint pairs to be reversed. Earlier comparisons separately classify website traces and fixed-duration unidirectional flow snapshots. (Sections 4.1.1 and 5; Appendices C.1–C.3)",
        "Input representation": "The aligned transfer input contains inter-arrival times, payload sizes and packet directions, with MinMax normalisation used by default. (Section 5.2.5)",
        "Packets / bytes": "Aligned inputs contain the first 30 non-empty packets of each bidirectional flow, giving a shared input shape of (30,3). (Sections 5.2.5 and 5.3)",
        "Preprocessing / anonymisation": "Orange is relabelled using CESNET's SNI mapping, common frequent classes are selected and CESNET is undersampled into balanced splits. Inter-arrival times are capped at 5 seconds, negative CESNET values become zero and Orange inputs are reconstructed to match CESNET's payload-bearing packets. (Sections 5.2.3–5.2.5)",
        "Architecture": "The study designs First Model, More Blocks, New Run and NoMB variants from UWTransformer, also called Full Model. Architectures combine channel-wise multi-head attention, convolutional layers, residual connections and dense classification layers. (Section 5.3; Table 7; Appendices F and H)",
        "Parameters": "Total parameter counts are 60,439 for First Model, 62,001 for MoreBlocks, 12,117 for NewRun, 121,801 for NoMB and 8,222,873 for Full Model. (Appendix H; Tables 10, 12, 14, 15 and 16)",
        "Training / evaluation datasets": "Earlier comparisons use Undefended with 95 website classes, ISCX-Flowpic Tor with 5 application categories and Orange June with 8 service categories. The aligned transfer framework uses 25 common service classes from CESNET and Orange June/October, with 1.2 million, 69.1K and 83.6K selected flows, respectively. (Sections 4.1 and 5.2; Tables 2 and 6)",
        "Split strategy": "CESNET training/validation and test data come from the first and last three collection days, respectively, with a 4:1 training/validation ratio. For transfer evaluation, models train on CESNET and are tested on the entire aligned Orange selection; snapshot experiments keep origin flows separate across training and test. (Sections 5.2.3 and 6.2; Section 4.2.1; Appendix D)",
        "Metrics": "The study reports accuracy, precision, recall and F1-score. Snapshot comparisons explicitly use the unweighted average of classwise F1-scores. (Section 4.2.3; Figures 5–7; Tables 8 and 9)",
        "Hardware": "GPU computation is reported, without a GPU model specification. (Appendix F)",
        "Latency": "UWTransformer's average training computation time is 18 milliseconds per batch of 64 samples, compared with 5 milliseconds for DFattack on the authors' GPU. (Appendix F)",
        "Measurement scope": "The reported computation time measures GPU training of a batch; no live classification pipeline timing is provided. (Appendix F)",
        "Deployment limitations": "Distribution shift substantially degrades classification even without concept drift, and task-related knowledge is insufficient for reliable use. Best performance also depends on training choices and hyperparameters that may be unavailable under realistic conditions. (Sections 4.4 and 7)",
        "Evaluation setting": "DFattack, Flowpic and UWTransformer are first retrained and compared across alternative datasets, separating snapshot classification from flow/trace classification. The aligned service-identification framework then compares transformer variants, XGBoost and cosine-distance 1-NN through same-dataset and cross-network evaluation, including reverse transfer and grouped-label tasks. (Sections 4, 5 and 6; Tables 1, 7–9)",
        "Leakage / shortcut risks": "The authors identify dataset-specific characteristics, selection cutoffs and hyperparameter choices as causes of inflated same-dataset performance. They prevent snapshots from the same flow crossing training/test boundaries, but explicitly derive snapshot validation data without respecting origin flows. (Sections 4.2.1, 4.4 and 7; Appendix D)"
}, url['onetask'], "Full text; field locators in each value")
    detail('platforms', {
        "Traffic unit definition": "Per-video streaming flow, classified using handshake messages from the initial connection establishment phase. (Section 2)",
        "Input representation": "A total of 62 attributes derived from TCP/QUIC and TLS ClientHello handshake fields, consisting of 20 numerical, 31 categorical (mapped to integers or presence flags), and 11 list fields encoded as fixed-length positional vectors. (Section 4.2; Table 2)",
        "Packets / bytes": "Classification uses handshake messages extracted from the first fewer than 5 packets of the connection setup. (Section 3.2.2)",
        "Preprocessing / anonymisation": "Packets are parsed to identify video flows by port number and TLS SNI, then split into handshake packets for classification and data packets for telemetry, with campus traffic analyzed without user identities. (Section 4.1)",
        "Architecture": "A bank of twelve Random Forest classifiers (three per streaming provider) predicting composite user platform, device type, and software agent, falling back to separate predictions if composite confidence is below 80%. (Section 4.1)",
        "Training / evaluation datasets": "A lab dataset of nearly 10,000 video flows across 30 user platforms for YouTube, Netflix, Disney+, and Amazon Prime Video; an open-set home dataset with over 2,000 flows; and a 4-month campus deployment capturing over 100 million video flows. (Section 3.1; Section 4.3.2; Section 5.2)",
        "Split strategy": "10-fold cross-validation on the lab dataset, supplemented by open-set evaluation on a distinct home network dataset. (Section 4.3.1; Section 4.3.2)",
        "Metrics": "Overall classification accuracy and prediction confidence (probability of the predicted class). (Section 4.1; Section 4.3.1)",
        "Hardware": "A commodity blade server equipped with an 8-core Intel Xeon E5-2620 CPU, 64 GB DDR4 RAM, and two 10 Gbps network interfaces. (Section 5.1)",
        "Throughput": "A peak real-time processing throughput of 20 Gbps and over 1,000 concurrent video flows during live campus deployment. (Section 4.3.3)",
        "Measurement scope": "Live end-to-end pipeline covering packet parsing, attribute generation, classification, and telemetry logging using DPDK, NFF-Go, Golang, and scikit-learn. (Section 5.1)",
        "Deployment limitations": "Performance degrades over time due to concept drift caused by software and firmware updates, requiring periodic retraining, while novel streaming services and platforms require new ground truth data collection. (Section 5.3)",
        "Evaluation setting": "Benchmarked against six state-of-the-art methods ([6], [14], [28], [40], [53], [55]) adapted to handle QUIC Initial packets, extract flow-level TLS ClientHello features, and predict user platforms. (Section 4.3.4; Table 6)"
}, url['platforms'], "Full text; field locators in each value")
    detail('simple', {
        "Traffic unit definition": "Flow-level: each sample is a network flow represented by the packet sizes, inter-packet times and directions of its first N (up to 30) payload packets. (Section 3.1)",
        "Input representation": "Raw packet-sequence metadata vector (sizes, IPTs in milliseconds, directions as ±1) compared with L1 distance, reweighted by per-dataset factors DIRscale and IPTscale with IPTs clipped at IPTmaxclip. (Section 3.1)",
        "Packets / bytes": "Only the first N payload packets per flow are used, no payload or header bytes; default N=10 from prior work, Optuna-tuned per dataset to values 5 to 27 in Table 2. (Section 3.1; Table 2)",
        "Preprocessing / anonymisation": "Datasets taken as curated pre-split tcbench versions; PCAPs converted to flow packet sequences with ipfixprobe; flows shorter than 10 packets filtered for MIRAGE19/22 and UTMOBILENET21, and empty flows and broadcasts filtered for CIC-IDS-2017; no IP or port masking described. (Sections 3.2-3.3)",
        "Architecture": "Non-parametric k-NN with L1 distance implemented as a Faiss index; prediction is the label of the top-1 nearest training sample, optionally replaced by distance-based majority voting among all training samples within a threshold Tmaj. (Sections 3.2, 3.5)",
        "Training / evaluation datasets": "12 datasets and 15 tasks (Table 1): CESNET-TLS22 (TLS, 191 classes), CESNET-QUIC22 (QUIC, 102), ISCXVPN2016 (VPN, 2 classes, three label tasks), MIRAGE19 (Android apps, 20), MIRAGE22 (video-meeting apps, 9), UTMOBILENET21 (mobile apps, 17), UCDAVIS19 (QUIC, 5 classes, Script and Human test sets), AppClassNet (TLS, 500 apps), EdgeIIoTset (IIoT, 15), UNSW-NB15 (attacks, 10), CIC-IDS-2017 (attacks, 8), CIC-DoHBrw-2020 (DoH, 2). (Abstract; Section 3.3; Table 1)",
        "Split strategy": "Flow-level splits per Table 1: CESNET-TLS22/QUIC22 time-based (1M/0.1M/1M), MIRAGE19/22 and UTMOBILENET21 prepared random 80/10/10, ISCXVPN2016 random 60/20/20, UCDAVIS19 fixed (7k train, 83 or 150 test), AppClassNet and EdgeIIoTset random 1M/0.1M/1M, UNSW-NB15, CIC-IDS-2017 and CIC-DoHBrw random 0.5M/0.1M/0.5M; results averaged over five repetitions (one for UCDAVIS19). (Section 3.3; Table 1)",
        "Metrics": "Accuracy is the primary metric, with F1 for three comparisons (MIRAGE19, MIRAGE22, UTMOBILENET21); the paper also defines maximum achievable accuracy (Eq. 1) and a minimal false positive rate estimate; no macro, weighted or micro averaging is stated. (Sections 3.6, 4.2)",
        "Evaluation setting": "Evaluation and critique study: the input-space k-NN baseline (default N=10, Optuna-tuned, and with distance-based majority voting) is tested on 12 datasets and 15 tasks against published SOTA numbers under replicated preprocessing and splitting; ISCXVPN2016 is also compared against payload-free SOTA in Table 4. (Section 3.6; Table 4)",
        "Deployment limitations": "The L1 metric cannot capture differences across packet positions such as missed and retransmitted packets or shifted patterns in the sequence, so the baseline misses such variations. (Section 3.1)",
        "Leakage / shortcut risks": "Authors report and test that most datasets contain over 50% exact duplicate packet sequences which random splits place in both training and test sets, trivially inflating accuracy for distance-based classifiers; duplicate fraction correlates with baseline performance, and on CESNET-QUIC22 the random split gives 79.41 versus 75.53 under a time-based split. Mixed-class duplicates cap maximum achievable accuracy, e.g. 93.46% on UTMOBILENET21. (Abstract; Sections 4.1-4.2, 5.1.2; Tables 5, 8)",
        "Version notes": "Table 3 reports F1 for MIRAGE19/MIRAGE22/UTMOBILENET21 while Table 5 recomputes accuracy for these without short-flow filtering (MIRAGE19 80.78 in Table 3 versus 78.56 in Table 5); UCDAVIS19 has no validation set, so it gets no Optuna tuning or majority voting and a single repetition; ISCXVPN2016 uses the preprocessed version of Nascita et al. (10.5k samples), not the original. (Table 5 footnote; Sections 3.3-3.4; Tables 1, 3, 5)"
}, url['simple'], "Full text; field locators in each value")
    detail('sugar', {
        "Traffic unit definition": "Packet classification and bidirectional flow classification; a flow comprises packets sharing the same 5-tuple, including both client and server packets. (Section 4.2, Downstream task)",
        "Input representation": "Packet bytes are converted into space-separated hexadecimal words and passed through the original T5 tokenizer. (Section 3.4, Phase 1)",
        "Packets / bytes": "Pcap-Encoder represents individual packets; flow classification uses majority voting over the first 5 packets. (Sections 3.4 and 6.2)",
        "Preprocessing / anonymisation": "The benchmark filters extraneous protocols, preserves test class distributions and avoids minimum packet or flow size filters. Pcap-Encoder pretraining randomises IP addresses and TTL values to discourage memorisation. (Section 4.1, Data cleaning and Sampling; Section 3.4, footnote 6; Appendix A.4)",
        "Architecture": "Pcap-Encoder uses T5-base with a mean pooling bottleneck and a two-layer MLP classification head with ReLU activation. (Section 3.4; Figure 2)",
        "Pretraining objective": "Sequential packet reconstruction using token cross-entropy, followed by question answering about protocol header fields and computations. (Section 3.4, Phases 1 and 2; Appendix A.1.3; Table 10)",
        "Pretraining datasets": "MAWI, UNSW-NB15 and a freshly collected campus trace are used for both pretraining phases. (Section 3.4, Phases 1 and 2)",
        "Fine-tuning objective": "Separate downstream classifiers are trained for each task, using binary cross-entropy or softmax according to the number of classes. (Section 3.4, Downstream classifiers)",
        "Training / evaluation datasets": "ISCX-VPN supplies VPN-binary, VPN-service and VPN-app tasks with 2, 6 and 16 classes; USTC-TFC supplies binary and application tasks with 2 and 20 classes. CSTN-TLS1.3 supplies TLS-120 website classification with 120 classes. (Section 4.1; Table 2)",
        "Split strategy": "The principal protocol uses a random per-flow 7:1 training/test split, balances training classes by undersampling and applies 3-fold cross-validation within training. A comparison protocol uses a random per-packet 8:1:1 training/validation/test split. (Section 5, Downstream task evaluation)",
        "Metrics": "Accuracy and macro-averaged F1-score, with the latter giving equal weight to each class. (Section 4.2, Performance metrics; Table 3)",
        "Reported results": "With frozen encoders and per-flow splitting, Pcap-Encoder achieves packet accuracy/macro F1 of 83.5%/71.0% on VPN-app and 71.0%/63.7% on TLS-120. Flow classification achieves 69.2%/62.2% and 71.3%/68.1%, respectively. (Tables 3 and 9; Sections 6.1 and 6.2)",
        "Hardware": "Experiments use an HPC cluster equipped with NVIDIA Tesla V100 SXM2 GPUs. (Section 6, opening paragraph)",
        "Measurement scope": "Efficiency compares training and inference time for completing cross-validation on VPN-app with per-flow splitting, normalised to Random Forest. (Section 6.3; Figure 6)",
        "Deployment limitations": "Pcap-Encoder's complexity and performance comparable to shallow models call its practicality into question; it is the second slowest evaluated model at both training and inference. (Sections 6.3 and 8)",
        "Evaluation setting": "ET-BERT, YaTC, NetMamba, TrafficFormer and netFound are evaluated alongside Pcap-Encoder and shallow baselines, using shared splits and original pretrained checkpoints. Packet and flow classification compare frozen and unfrozen encoders, with per-flow and per-packet splitting examined for packet classification. (Section 5; Sections 6.1 and 6.2; Tables 3–9)",
        "Leakage / shortcut risks": "Per-packet splitting lets models associate test packets with training flows through explicit identifiers and implicit identifiers such as TCP sequence numbers, acknowledgement numbers and timestamps. The authors test these shortcuts by randomising the implicit identifiers and also identify pretraining/downstream dataset reuse as a leakage risk. (Sections 3.2, 4.1 and 6.1; Table 6; Figure 5)"
}, url['sugar'], "Full text; field locators in each value")
    detail('trafficgpt', {
        "Traffic unit definition": "A traffic flow is defined by the network five-tuple, representing a sequence of packets that share identical source and destination IP addresses, ports, and protocols. (Section III-B)",
        "Input representation": "Each flow is converted into a reversible sequence of 260 discrete tokens, structured as packet start tokens, link-type tokens, 8-byte exponential time interval tokens, hexadecimal byte tokens for header and payload, and an end token. (Section III-B)",
        "Packets / bytes": "Pre-training accommodates maximum token sequence lengths of 3,072 or 12,032 tokens, whereas fine-tuning evaluations predominantly use a maximum token length of 256. (Section IV-A; Section IV-B)",
        "Preprocessing / anonymisation": "Packets from protocols other than TCP or UDP (such as ARP and DHCP) are discarded. In classification evaluations, MAC addresses, IP addresses, and port information are stripped to avoid shortcut learning. (Section IV-A; Section IV-B)",
        "Architecture": "TrafficGPT is an auto-regressive model using linear attention with local attention and reversible residual layers. It has 24 layers, a hidden dimension of 512, 12 attention heads, 8 local attention heads with a local window of 256, an embedding dimension of 256, and token shifting. (Section III-A; Section IV-A)",
        "Pretraining objective": "Auto-regressive self-supervised language modelling trained to predict the next token via cross-entropy loss. (Section III-C)",
        "Pretraining datasets": "A compilation of five public datasets totalling 189 GB: ISCXTor2016, USTCTFC2016, ISCXVPN2016, DoHBrw2020, and CICIoT2022. (Section IV-A)",
        "Fine-tuning objective": "A classification task where a [cls] token is prepended to the flow tokens and the model predicts the class label at the next output position. (Section III-E)",
        "Training / evaluation datasets": "Evaluations are performed on Cross-Platform iOS (196 classes), Cross-Platform Android (215 classes), ISCX-VPN-App (13 classes), and USTC-TFC (20 classes). (Section IV-B)",
        "Split strategy": "Flow-level partition where 99% of flows are allocated to pre-training and 1% are reserved for testing. (Section IV-A)",
        "Metrics": "Macro F1-score and accuracy (AC) for classification; Jensen-Shannon Divergence (JSD) for packet headers and flow features in generation. (Section IV-B; Table I; Section IV-C)",
        "Reported results": "TrafficGPT(12k) achieved Macro F1-scores of 0.9863 on Cross-Platform (iOS), 0.9498 on Cross-Platform (Android), 1.0000 on ISCX-VPN-App, and 0.9877 on USTC-TFC. (Section IV-B; Table I)",
        "Deployment limitations": "The model operates only on individual TCP and UDP flows, missing multi-flow correlations, and exhibits anomalies generating encrypted traffic, such as malformed TLS Client Hello packets. (Section IV-C; Section V)",
        "Leakage / shortcut risks": "Models may exploit dataset shortcuts such as IP addresses or MAC addresses; hence, these fields were removed during preprocessing. (Section IV-B)"
}, url['trafficgpt'], "Full text; field locators in each value")
