"""Papers accepted from discovery review issue #1 (2026-10-19), Task 19.

Bylines, venues and years are read from the PDFs in corpus/ (arXiv v1/v2 or the publisher version).
Every field paraphrases the paper's own abstract. Datasets and relationships are recorded only when
the abstract names them; full-text extraction is left for later tasks.
"""
CHECKED = '2026-10-19'
PRE = 'Preprint; venue not verified'
CN = 'Computer Networks'

NEW = ['netagent', 'joivcompare', 'supclgnn', 'scsm', 'vfrdad', 'distilshortcut', 'shortcutgen',
       'netlexicon', 'curvtail', 'pmpnet', 'dpft', 'netcofi']


def add_papers(add, rel, E):
    add('netagent', 'NetAgent', 'NetAgent: Multi-Task Agentic Network Traffic Analysis Made Practical',
        'Hao Fu|Dawn Song|Peng Gao', 2026, 'arXiv', 'https://arxiv.org/abs/2610.07386v1',
        'Deep learning', 'Multiple',
        'Proposes an agentic framework that handles many traffic analysis tasks, from intrusion detection to encrypted traffic classification, without task-specific training.',
        'An agent loop plans and decomposes tasks using attack knowledge, 150+ tools extracted from 50+ published systems, a code execution space, three-tier memory and sandboxed runtime repair. Across 9 benchmarks it reports 90.04% F1 on unseen traffic distributions against 2.74% and 3.04% for the best single-task and multi-task baselines.',
        'Results are the authors’ own agentic setup; cost, latency and dependence on the underlying language model are not given in the abstract.',
        'What an agentic pipeline costs per decision, and how it behaves when the tools it calls fail under shift.',
        publicationStatus=PRE, task='Multi-task traffic analysis', crossDataset='Yes',
        techniques=['Foundation models', 'Multitask learning', 'Distribution shift'])
    add('joivcompare', 'Transformer comparison (JOIV)', 'A Comparative Study on Transformer-Based Deep Learning Model for Network Traffic Classification',
        'Muhammad Alif Ikhwan Zainuddin|Mohd Rizal Mohd Isa|Nur Diyana Kamarudin|Fazilatulaili Ali|Muhammad Fendi Osman|Mukhtar Nazifi Imam',
        2026, 'JOIV: International Journal on Informatics Visualization 10(5)', 'https://doi.org/10.62527/joiv.10.5.4411',
        'Evaluation & surveys', 'Flow',
        'Compares ANN, CNN, RNN and Transformer classifiers on encrypted traffic flows.',
        'Uses a telemetry dataset from Jabatan Data Negara, Malaysia: 12,000 encrypted flows across 648 application classes, split with balanced stratified sampling. The Transformer reaches 99.60% accuracy; the 1D CNN 65.13%; an RNN with 2,803 parameters is presented as the edge option.',
        'One dataset; the abstract does not state how the 12.4 Gbps throughput figure was measured.',
        'Whether the ranking holds on public collections and under a capture-time split.',
        publicationStatus='Peer reviewed', techniques=['Transformers', 'CNN', 'RNN / LSTM'])
    add('supclgnn', 'SupCL-GNN', 'SupCL-GNN: Supervised contrastive learning with graph neural networks for enhanced encrypted traffic classification',
        'Guolong Li|Yuan Gao|Jiongjiong Ren|Shaozhen Chen', 2026, f'{CN} 291', 'https://doi.org/10.1016/j.comnet.2026.112816',
        'Graph learning', 'Flow',
        'Combines supervised contrastive learning with graph neural networks to learn noise-robust traffic features.',
        'A Traffic Distribution Graph fuses encoded packet bytes and packet-length sequences so that classes form distinct topologies. Evaluated on ISCX-VPN2016, ISCX-Tor2016, USTC-TFC2016 and MOBILE-APP.',
        'The abstract reports outperforming baselines without numbers; robustness is argued from the training objective.',
        'Whether graph topology separates classes once capture-specific byte fields are removed.',
        publicationStatus='Peer reviewed', datasets=['iscxvpn', 'iscxtor', 'ustc'],
        techniques=['Graph learning', 'Contrastive learning', 'Raw packet bytes'])
    add('scsm', 'SCSM', 'SCSM: A Traffic-Native Foundation Model for Transferable Website Fingerprinting',
        'Xianwen Deng|Ruijie Zhao|Mingwei Zhan|Yijun Wang|Zhi Xue', 2026, 'arXiv', 'https://arxiv.org/abs/2610.07776v1',
        'State space', 'Multi-flow',
        'Pretrains a traffic-native foundation model for website fingerprinting that transfers across website sets, time, paths, browsers and defences.',
        'Pretraining views are built from unlabelled traces by Segmentation, Combination, Scaling and Masking; windowed traffic counting matrices train a state-space encoder contrastively, then a small labelled support set fine-tunes it. Reports +16.4% average top-3 accuracy over six temporal-drift tasks on GTT23 and +13.8% average macro-F1 over four cross-domain datasets.',
        'Code and data are announced but not yet released; gains are relative to the strongest baselines the authors ran.',
        'How far few-shot adaptation holds once defences are tuned against the pretrained encoder.',
        publicationStatus=PRE, task='Website fingerprinting', pretraining='Yes', crossDataset='Yes',
        techniques=['Foundation models', 'State-space models', 'Contrastive learning', 'Timing and direction sequences'])
    add('vfrdad', 'VFRDAD', 'VFRDAD: An IoT Encrypted traffic identification method based on multi-scale local information and enhanced global information fusion',
        'Jiangjin Gao|Yong Liu|Rui Jiang|Tao Yang|Jianjiang Zheng', 2026, f'{CN} 290', 'https://doi.org/10.1016/j.comnet.2026.112782',
        'Transformer', 'Session',
        'Classifies IoT encrypted traffic from session-level grayscale images by fusing local and global features.',
        'Multi-scale high-pass filtering captures local patterns; a traffic-domain autoencoder and dilated convolutions build a three-channel image for a Vision Transformer; gated attention fuses both. Evaluated on Darknet-dataset-2020, ISCXVPN2016 and CIC-IoT-2023.',
        'Image representations of raw sessions can carry capture-specific bytes; the abstract reports gains under the evaluated protocols only.',
        'Which image regions drive the decision once headers are masked.',
        publicationStatus='Peer reviewed', datasets=['iscxvpn'],
        techniques=['Transformers', 'CNN', 'Autoencoding', 'Raw packet bytes'])
    add('distilshortcut', 'Distillation over one year', 'Unknown-Traffic Detection, Calibration and Shortcut Reliance in Distilled Encrypted-Traffic Classifiers over One Year',
        'Mahmoud Abbasi', 2026, 'arXiv', 'https://arxiv.org/abs/2609.31141v1',
        'Evaluation & surveys', 'Flow',
        'Tests what a distilled student inherits from its teacher beyond accuracy: unknown-traffic detection, calibration, shortcut reliance and behaviour under a year of drift.',
        'One 101k-parameter student is distilled from two equally accurate teachers (a five-member ensemble and a wider single model). Ten pre-registered hypotheses are tested on CESNET-TLS-Year22 over 18 test windows across 35 weeks; two are supported, and shortcut reliance follows model size, not distillation.',
        'Single dataset and one student size; transfer findings depend on the scoring rule (logit-based versus feature-space detectors).',
        'Whether the same inheritance pattern appears for pretrained traffic foundation models compressed for the edge.',
        publicationStatus=PRE, task='Knowledge distillation study', openWorld='Yes',
        techniques=['Open-world recognition', 'Concept drift', 'Data leakage control'])
    add('shortcutgen', 'Shortcut in Generalization', 'Shortcut in Generalization: Rethinking Evaluation Protocol for Encrypted Traffic Classification',
        'Qiming Yu|Chungang Lin|Zhengyi Ma|Zijia Song|Yuliang Lu|Guozheng Yang|Dongzhen Qi', 2026, 'arXiv', 'https://arxiv.org/abs/2610.17961v1',
        'Evaluation & surveys', 'Packet / flow',
        'Studies how evaluation protocols inflate encrypted traffic classification results through field-level shortcuts, cross-partition sharing and test-only transformations.',
        'Compares feature importance, retrained feature removal and field-only split sensitivity on three public datasets, varying Source-IP overlap and packets per flow. Raising Source-IP overlap from 0% to 100% adds about 32–33 accuracy points before identifier masking and about 8 after; for YaTC and NetMamba the 11–13 point loss from test-only IP zeroing is almost fully recovered when the same transformation is applied in training.',
        'The three datasets are not named in the abstract; results cover the methods the authors retrained.',
        'An evaluation protocol that fixes sharing and train–test processing before any model comparison.',
        publicationStatus=PRE, task='Shortcut diagnosis and mitigation',
        techniques=['Data leakage control', 'Header fields', 'Reproducibility'])
    rel('shortcutgen', 'yatc', 'Diagnoses', 'Shows YaTC’s 11–13 point loss under test-only IP zeroing is almost fully recovered when training applies the same transformation.', 'https://arxiv.org/abs/2610.17961v1', 'Abstract')
    rel('shortcutgen', 'netmamba', 'Diagnoses', 'Shows NetMamba’s 11–13 point loss under test-only IP zeroing is almost fully recovered when training applies the same transformation.', 'https://arxiv.org/abs/2610.17961v1', 'Abstract')
    add('netlexicon', 'NetLexicon', 'NetLexicon: Learning Discrete Behavioral Representations for Encrypted Web Traffic Analysis',
        'Xiangyu Gao|Tong Li|Ziqiang Wang|Yinchao Zhang|Rongbang Wu|Zhenxing Zhang|Jing Hu|Hanlin Huang|Xinle Du|Su Yao|Qi Li|Ke Xu',
        2026, 'arXiv', 'https://arxiv.org/abs/2609.37672v1',
        'Self-supervised', 'Flow',
        'Pretrains discrete behavioural states from unlabelled encrypted Web traffic as a compact traffic lexicon.',
        'Vector quantisation turns contextual traffic windows into discrete states, trained with State Transition Prediction and Statistical Feature Alignment. On four benchmarks (Web application, service type, malware) it reports up to 25.5 points higher macro-F1 than the strongest baseline and up to 23.6× less fine-tuning time per epoch.',
        'Benchmarks are not named in the abstract; interpretability is shown by inspecting learned states.',
        'Whether a learned traffic lexicon stays stable across capture sites and years.',
        publicationStatus=PRE, pretraining='Yes',
        techniques=['Self-supervised learning', 'Learned tokenisation', 'Timing and direction sequences'])
    add('curvtail', 'Curv-Tail', 'Curv-Tail: Lightweight Long-Tailed Encrypted Traffic Classification with Discrete Packet-Length Encoding and Lorentz Prototypes',
        'Yankun Wang|Jun-Jie Huang|Lin Liu|Xiaodong Lei|Yi Chen|Yeqing Yan|Lin Liu|Jiangyong Shi|Yongjun Wang',
        2026, 'arXiv', 'https://arxiv.org/abs/2609.32242v2',
        'Deep learning', 'Packet / flow',
        'Targets long-tailed encrypted traffic classification under a small compute budget, without a separate pretraining stage.',
        'Mixed-resolution tokens keep exact packet lengths within a bounded range; an auxiliary task predicts length tokens; compact temporal encoders read packet sequences and directional byte patches, classified by Lorentz prototypes. Three-seed mean Tail-F1 is 85.70% on NUDT-Mobile and 46.30% on DataCon-Website; on an RTX 4090 it uses 98.48% fewer parameters and 10.2× the batch inference throughput of MM4Flow.',
        'Throughput is offline batch inference (FP32, batch 256), not a live rate.',
        'How tail-class accuracy holds when the head classes drift over time.',
        publicationStatus=PRE, pretraining='No',
        techniques=['Timing and direction sequences', 'Raw packet bytes', 'Learned tokenisation'],
        details={'Version notes': 'Reviewed arXiv v2 (10 October 2026). The third and seventh authors, both named Lin Liu, are different people (paper footnote).'})
    rel('curvtail', 'mm4flow', 'Compares against', 'Reports 98.48% fewer parameters and 10.2× the batch inference throughput of MM4Flow in 300-class profiling.', 'https://arxiv.org/abs/2609.32242v2', 'Abstract')
    add('pmpnet', 'PMP-Net', 'PMP-Net: A packet-level multi-branch prototype network for few-shot and open-set encrypted traffic classification',
        'Hongxiu Yang|Zihe Ren|Zehua Du|Xinghai Yang|Kaixiang Jiang', 2026, f'{CN} 290', 'https://doi.org/10.1016/j.comnet.2026.112798',
        'Deep learning', 'Packet',
        'Classifies individual encrypted packets in few-shot and open-set settings.',
        'Separate branches read packet headers and payloads, joined by bidirectional multi-head attention; prototypes with a similarity-threshold rejection flag unknown classes. Reports 98.9% and 99.2% accuracy on ISCX and USTC-TFC2016 with millisecond-level inference latency.',
        'Packet-level header input can expose identifiers; the abstract does not say which ISCX collection is used.',
        'Whether the rejection threshold holds for unknown classes from a different capture.',
        publicationStatus='Peer reviewed', openWorld='Yes', datasets=['ustc'],
        techniques=['Open-world recognition', 'Meta-learning', 'Header and payload'])
    add('dpft', 'DPFT', 'DPFT: A dual-phase transformer with pre-training and structurally adaptive fine-tuning for encrypted traffic classification',
        'Hui Zhao|Ao Yin', 2026, f'{CN} (journal pre-proof)', 'https://doi.org/10.1016/j.comnet.2026.112844',
        'Transformer', 'Burst / flow',
        'Couples traffic-oriented pretraining with a fine-tuning structure designed for downstream classification.',
        'Pretraining combines Masked Burst Prediction and Burst Structural Discrimination; fine-tuning adds dynamic embedding fusion and multi-head attention pooling. Within-dataset closed-set macro-F1: CSTNET-TLS 1.3 93.10%, ISCX-VPN-App 97.92%, ISCX-VPN-Service 95.65%, USTC-TFC 2016 98.87%.',
        'The authors state that robustness to temporal or cross-domain shift, unseen classes and deployment conditions remains unverified.',
        'Whether burst-structure pretraining helps under a capture-disjoint split.',
        publicationStatus='Peer reviewed', pretraining='Yes', datasets=['cstnet', 'iscxvpn', 'ustc'],
        techniques=['Transformers', 'Masked language modelling', 'Burst representations'],
        details={'Version notes': 'Journal pre-proof (accepted 5 October 2026); not yet the version of record.'})
    add('netcofi', 'NetCoFi', 'NetCoFi: A Budget-Aware Coarse-Fine Dual-Branch Model for Encrypted Traffic Classification',
        'Zhengyi Ma|Qiming Yu|Chungang Lin|Wentao Cui|Zijia Song|Guozheng Yang', 2026, 'arXiv', 'https://arxiv.org/abs/2610.17978v1',
        'State space', 'Flow',
        'Lets one encrypted traffic classifier trade accuracy for compute at inference time.',
        'Byte representations and packet metadata select token neighbourhoods for fine-grained encoding while the full window is compressed into coarse context; multi-budget training serves several routing budgets without retraining. Six public datasets; at low budgets +7.86 macro-F1 points over a same-depth static baseline on three; in a DPDK–GPU pipeline mean batch throughput rises from 26.42 to 43.42 Mb/s, 1.64× NetMamba.',
        'Datasets are not named in the abstract; throughput is mean batch throughput in the authors’ pipeline.',
        'How routing budgets should be set when traffic mix changes during deployment.',
        publicationStatus=PRE, deployment='Yes',
        techniques=['State-space models', 'Raw packet bytes', 'Resource-aware scheduling', 'Deployment'])
    rel('netcofi', 'netmamba', 'Compares against', 'Reports 1.64× NetMamba’s mean batch throughput (26.42 to 43.42 Mb/s) in a DPDK–GPU pipeline.', 'https://arxiv.org/abs/2610.17978v1', 'Abstract')
    for e in E:
        if e['paperId'] in NEW: e['accessed'] = CHECKED
