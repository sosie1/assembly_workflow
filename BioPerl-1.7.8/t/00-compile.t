use 5.006;
use strict;
use warnings;

# this test was generated with Dist::Zilla::Plugin::Test::Compile 2.058

use Test::More;

plan tests => 511 + ($ENV{AUTHOR_TESTING} ? 1 : 0);

my @module_files = (
    'Bio/Align/AlignI.pm',
    'Bio/Align/DNAStatistics.pm',
    'Bio/Align/PairwiseStatistics.pm',
    'Bio/Align/ProteinStatistics.pm',
    'Bio/Align/StatisticsI.pm',
    'Bio/Align/Utilities.pm',
    'Bio/AlignIO.pm',
    'Bio/AlignIO/Handler/GenericAlignHandler.pm',
    'Bio/AlignIO/arp.pm',
    'Bio/AlignIO/bl2seq.pm',
    'Bio/AlignIO/clustalw.pm',
    'Bio/AlignIO/emboss.pm',
    'Bio/AlignIO/fasta.pm',
    'Bio/AlignIO/largemultifasta.pm',
    'Bio/AlignIO/maf.pm',
    'Bio/AlignIO/mase.pm',
    'Bio/AlignIO/mega.pm',
    'Bio/AlignIO/meme.pm',
    'Bio/AlignIO/metafasta.pm',
    'Bio/AlignIO/msf.pm',
    'Bio/AlignIO/nexus.pm',
    'Bio/AlignIO/pfam.pm',
    'Bio/AlignIO/phylip.pm',
    'Bio/AlignIO/po.pm',
    'Bio/AlignIO/proda.pm',
    'Bio/AlignIO/prodom.pm',
    'Bio/AlignIO/psi.pm',
    'Bio/AlignIO/selex.pm',
    'Bio/AlignIO/xmfa.pm',
    'Bio/AnalysisI.pm',
    'Bio/AnalysisParserI.pm',
    'Bio/AnalysisResultI.pm',
    'Bio/AnnotatableI.pm',
    'Bio/Annotation/AnnotationFactory.pm',
    'Bio/Annotation/Collection.pm',
    'Bio/Annotation/Comment.pm',
    'Bio/Annotation/DBLink.pm',
    'Bio/Annotation/OntologyTerm.pm',
    'Bio/Annotation/Reference.pm',
    'Bio/Annotation/Relation.pm',
    'Bio/Annotation/SimpleValue.pm',
    'Bio/Annotation/StructuredValue.pm',
    'Bio/Annotation/TagTree.pm',
    'Bio/Annotation/Target.pm',
    'Bio/Annotation/Tree.pm',
    'Bio/Annotation/TypeManager.pm',
    'Bio/AnnotationCollectionI.pm',
    'Bio/AnnotationI.pm',
    'Bio/CodonUsage/IO.pm',
    'Bio/CodonUsage/Table.pm',
    'Bio/DB/DBFetch.pm',
    'Bio/DB/Failover.pm',
    'Bio/DB/Fasta.pm',
    'Bio/DB/FileCache.pm',
    'Bio/DB/Flat.pm',
    'Bio/DB/Flat/BDB.pm',
    'Bio/DB/Flat/BDB/embl.pm',
    'Bio/DB/Flat/BDB/fasta.pm',
    'Bio/DB/Flat/BDB/genbank.pm',
    'Bio/DB/Flat/BDB/swiss.pm',
    'Bio/DB/Flat/BinarySearch.pm',
    'Bio/DB/GFF/Util/Binning.pm',
    'Bio/DB/GFF/Util/Rearrange.pm',
    'Bio/DB/GenericWebAgent.pm',
    'Bio/DB/InMemoryCache.pm',
    'Bio/DB/IndexedBase.pm',
    'Bio/DB/LocationI.pm',
    'Bio/DB/Qual.pm',
    'Bio/DB/Query/WebQuery.pm',
    'Bio/DB/QueryI.pm',
    'Bio/DB/RandomAccessI.pm',
    'Bio/DB/ReferenceI.pm',
    'Bio/DB/Registry.pm',
    'Bio/DB/SeqI.pm',
    'Bio/DB/Taxonomy.pm',
    'Bio/DB/Taxonomy/flatfile.pm',
    'Bio/DB/Taxonomy/greengenes.pm',
    'Bio/DB/Taxonomy/list.pm',
    'Bio/DB/Taxonomy/silva.pm',
    'Bio/DB/UpdateableSeqI.pm',
    'Bio/DB/WebDBSeqI.pm',
    'Bio/DBLinkContainerI.pm',
    'Bio/Das/FeatureTypeI.pm',
    'Bio/Das/SegmentI.pm',
    'Bio/DasI.pm',
    'Bio/DescribableI.pm',
    'Bio/Event/EventGeneratorI.pm',
    'Bio/Event/EventHandlerI.pm',
    'Bio/Factory/AnalysisI.pm',
    'Bio/Factory/ApplicationFactoryI.pm',
    'Bio/Factory/DriverFactory.pm',
    'Bio/Factory/FTLocationFactory.pm',
    'Bio/Factory/LocationFactoryI.pm',
    'Bio/Factory/ObjectBuilderI.pm',
    'Bio/Factory/ObjectFactory.pm',
    'Bio/Factory/ObjectFactoryI.pm',
    'Bio/Factory/SeqAnalysisParserFactory.pm',
    'Bio/Factory/SeqAnalysisParserFactoryI.pm',
    'Bio/Factory/SequenceFactoryI.pm',
    'Bio/Factory/SequenceProcessorI.pm',
    'Bio/Factory/SequenceStreamI.pm',
    'Bio/Factory/TreeFactoryI.pm',
    'Bio/FeatureHolderI.pm',
    'Bio/HandlerBaseI.pm',
    'Bio/IdCollectionI.pm',
    'Bio/IdentifiableI.pm',
    'Bio/Index/Abstract.pm',
    'Bio/Index/AbstractSeq.pm',
    'Bio/Index/Blast.pm',
    'Bio/Index/BlastTable.pm',
    'Bio/Index/EMBL.pm',
    'Bio/Index/Fasta.pm',
    'Bio/Index/Fastq.pm',
    'Bio/Index/GenBank.pm',
    'Bio/Index/Qual.pm',
    'Bio/Index/SwissPfam.pm',
    'Bio/Index/Swissprot.pm',
    'Bio/LocatableSeq.pm',
    'Bio/Location/Atomic.pm',
    'Bio/Location/AvWithinCoordPolicy.pm',
    'Bio/Location/CoordinatePolicyI.pm',
    'Bio/Location/Fuzzy.pm',
    'Bio/Location/FuzzyLocationI.pm',
    'Bio/Location/NarrowestCoordPolicy.pm',
    'Bio/Location/Simple.pm',
    'Bio/Location/Split.pm',
    'Bio/Location/SplitLocationI.pm',
    'Bio/Location/WidestCoordPolicy.pm',
    'Bio/LocationI.pm',
    'Bio/Matrix/Generic.pm',
    'Bio/Matrix/IO.pm',
    'Bio/Matrix/IO/mlagan.pm',
    'Bio/Matrix/IO/phylip.pm',
    'Bio/Matrix/IO/scoring.pm',
    'Bio/Matrix/MatrixI.pm',
    'Bio/Matrix/Mlagan.pm',
    'Bio/Matrix/PSM/IO.pm',
    'Bio/Matrix/PSM/IO/mast.pm',
    'Bio/Matrix/PSM/IO/masta.pm',
    'Bio/Matrix/PSM/IO/meme.pm',
    'Bio/Matrix/PSM/IO/psiblast.pm',
    'Bio/Matrix/PSM/IO/transfac.pm',
    'Bio/Matrix/PSM/InstanceSite.pm',
    'Bio/Matrix/PSM/InstanceSiteI.pm',
    'Bio/Matrix/PSM/ProtMatrix.pm',
    'Bio/Matrix/PSM/ProtPsm.pm',
    'Bio/Matrix/PSM/Psm.pm',
    'Bio/Matrix/PSM/PsmHeader.pm',
    'Bio/Matrix/PSM/PsmHeaderI.pm',
    'Bio/Matrix/PSM/PsmI.pm',
    'Bio/Matrix/PSM/SiteMatrix.pm',
    'Bio/Matrix/PSM/SiteMatrixI.pm',
    'Bio/Matrix/PhylipDist.pm',
    'Bio/Matrix/Scoring.pm',
    'Bio/Ontology/DocumentRegistry.pm',
    'Bio/Ontology/GOterm.pm',
    'Bio/Ontology/InterProTerm.pm',
    'Bio/Ontology/OBOEngine.pm',
    'Bio/Ontology/OBOterm.pm',
    'Bio/Ontology/Ontology.pm',
    'Bio/Ontology/OntologyEngineI.pm',
    'Bio/Ontology/OntologyI.pm',
    'Bio/Ontology/OntologyStore.pm',
    'Bio/Ontology/Path.pm',
    'Bio/Ontology/PathI.pm',
    'Bio/Ontology/Relationship.pm',
    'Bio/Ontology/RelationshipFactory.pm',
    'Bio/Ontology/RelationshipI.pm',
    'Bio/Ontology/RelationshipType.pm',
    'Bio/Ontology/SimpleGOEngine/GraphAdaptor.pm',
    'Bio/Ontology/SimpleOntologyEngine.pm',
    'Bio/Ontology/Term.pm',
    'Bio/Ontology/TermFactory.pm',
    'Bio/Ontology/TermI.pm',
    'Bio/OntologyIO.pm',
    'Bio/OntologyIO/Handlers/BaseSAXHandler.pm',
    'Bio/OntologyIO/Handlers/InterProHandler.pm',
    'Bio/OntologyIO/Handlers/InterPro_BioSQL_Handler.pm',
    'Bio/OntologyIO/InterProParser.pm',
    'Bio/OntologyIO/dagflat.pm',
    'Bio/OntologyIO/goflat.pm',
    'Bio/OntologyIO/obo.pm',
    'Bio/OntologyIO/simplehierarchy.pm',
    'Bio/OntologyIO/soflat.pm',
    'Bio/ParameterBaseI.pm',
    'Bio/PrimarySeq.pm',
    'Bio/PrimarySeqI.pm',
    'Bio/PullParserI.pm',
    'Bio/Range.pm',
    'Bio/RangeI.pm',
    'Bio/Root/Exception.pm',
    'Bio/Root/HTTPget.pm',
    'Bio/Root/IO.pm',
    'Bio/Root/Root.pm',
    'Bio/Root/RootI.pm',
    'Bio/Root/Storable.pm',
    'Bio/Root/Test.pm',
    'Bio/Root/TestObject.pm',
    'Bio/Root/Utilities.pm',
    'Bio/Root/Version.pm',
    'Bio/Search/BlastStatistics.pm',
    'Bio/Search/BlastUtils.pm',
    'Bio/Search/DatabaseI.pm',
    'Bio/Search/GenericDatabase.pm',
    'Bio/Search/GenericStatistics.pm',
    'Bio/Search/HSP/BlastHSP.pm',
    'Bio/Search/HSP/BlastPullHSP.pm',
    'Bio/Search/HSP/FastaHSP.pm',
    'Bio/Search/HSP/GenericHSP.pm',
    'Bio/Search/HSP/HSPFactory.pm',
    'Bio/Search/HSP/HSPI.pm',
    'Bio/Search/HSP/ModelHSP.pm',
    'Bio/Search/HSP/PSLHSP.pm',
    'Bio/Search/HSP/PsiBlastHSP.pm',
    'Bio/Search/HSP/PullHSPI.pm',
    'Bio/Search/HSP/WABAHSP.pm',
    'Bio/Search/Hit/BlastHit.pm',
    'Bio/Search/Hit/BlastPullHit.pm',
    'Bio/Search/Hit/Fasta.pm',
    'Bio/Search/Hit/GenericHit.pm',
    'Bio/Search/Hit/HitFactory.pm',
    'Bio/Search/Hit/HitI.pm',
    'Bio/Search/Hit/ModelHit.pm',
    'Bio/Search/Hit/PsiBlastHit.pm',
    'Bio/Search/Hit/PullHitI.pm',
    'Bio/Search/Iteration/GenericIteration.pm',
    'Bio/Search/Iteration/IterationI.pm',
    'Bio/Search/Processor.pm',
    'Bio/Search/Result/BlastPullResult.pm',
    'Bio/Search/Result/BlastResult.pm',
    'Bio/Search/Result/CrossMatchResult.pm',
    'Bio/Search/Result/GenericResult.pm',
    'Bio/Search/Result/INFERNALResult.pm',
    'Bio/Search/Result/PullResultI.pm',
    'Bio/Search/Result/ResultFactory.pm',
    'Bio/Search/Result/ResultI.pm',
    'Bio/Search/Result/WABAResult.pm',
    'Bio/Search/SearchUtils.pm',
    'Bio/Search/StatisticsI.pm',
    'Bio/Search/Tiling/MapTileUtils.pm',
    'Bio/Search/Tiling/MapTiling.pm',
    'Bio/Search/Tiling/TilingI.pm',
    'Bio/SearchIO.pm',
    'Bio/SearchIO/EventHandlerI.pm',
    'Bio/SearchIO/FastHitEventBuilder.pm',
    'Bio/SearchIO/IteratedSearchResultEventBuilder.pm',
    'Bio/SearchIO/SearchResultEventBuilder.pm',
    'Bio/SearchIO/SearchWriterI.pm',
    'Bio/SearchIO/Writer/GbrowseGFF.pm',
    'Bio/SearchIO/Writer/HSPTableWriter.pm',
    'Bio/SearchIO/Writer/HTMLResultWriter.pm',
    'Bio/SearchIO/Writer/HitTableWriter.pm',
    'Bio/SearchIO/Writer/ResultTableWriter.pm',
    'Bio/SearchIO/Writer/TextResultWriter.pm',
    'Bio/SearchIO/axt.pm',
    'Bio/SearchIO/blast.pm',
    'Bio/SearchIO/blast_pull.pm',
    'Bio/SearchIO/blasttable.pm',
    'Bio/SearchIO/cross_match.pm',
    'Bio/SearchIO/erpin.pm',
    'Bio/SearchIO/exonerate.pm',
    'Bio/SearchIO/fasta.pm',
    'Bio/SearchIO/gmap_f9.pm',
    'Bio/SearchIO/infernal.pm',
    'Bio/SearchIO/megablast.pm',
    'Bio/SearchIO/psl.pm',
    'Bio/SearchIO/rnamotif.pm',
    'Bio/SearchIO/sim4.pm',
    'Bio/SearchIO/waba.pm',
    'Bio/SearchIO/wise.pm',
    'Bio/Seq.pm',
    'Bio/Seq/BaseSeqProcessor.pm',
    'Bio/Seq/EncodedSeq.pm',
    'Bio/Seq/LargeLocatableSeq.pm',
    'Bio/Seq/LargePrimarySeq.pm',
    'Bio/Seq/LargeSeq.pm',
    'Bio/Seq/LargeSeqI.pm',
    'Bio/Seq/Meta.pm',
    'Bio/Seq/Meta/Array.pm',
    'Bio/Seq/MetaI.pm',
    'Bio/Seq/PrimaryQual.pm',
    'Bio/Seq/PrimedSeq.pm',
    'Bio/Seq/QualI.pm',
    'Bio/Seq/Quality.pm',
    'Bio/Seq/RichSeq.pm',
    'Bio/Seq/RichSeqI.pm',
    'Bio/Seq/SeqBuilder.pm',
    'Bio/Seq/SeqFactory.pm',
    'Bio/Seq/SeqFastaSpeedFactory.pm',
    'Bio/Seq/SequenceTrace.pm',
    'Bio/Seq/SimulatedRead.pm',
    'Bio/Seq/TraceI.pm',
    'Bio/SeqAnalysisParserI.pm',
    'Bio/SeqFeature/Amplicon.pm',
    'Bio/SeqFeature/AnnotationAdaptor.pm',
    'Bio/SeqFeature/Collection.pm',
    'Bio/SeqFeature/CollectionI.pm',
    'Bio/SeqFeature/Computation.pm',
    'Bio/SeqFeature/FeaturePair.pm',
    'Bio/SeqFeature/Gene/Exon.pm',
    'Bio/SeqFeature/Gene/ExonI.pm',
    'Bio/SeqFeature/Gene/GeneStructure.pm',
    'Bio/SeqFeature/Gene/GeneStructureI.pm',
    'Bio/SeqFeature/Gene/Intron.pm',
    'Bio/SeqFeature/Gene/NC_Feature.pm',
    'Bio/SeqFeature/Gene/Poly_A_site.pm',
    'Bio/SeqFeature/Gene/Promoter.pm',
    'Bio/SeqFeature/Gene/Transcript.pm',
    'Bio/SeqFeature/Gene/TranscriptI.pm',
    'Bio/SeqFeature/Gene/UTR.pm',
    'Bio/SeqFeature/Generic.pm',
    'Bio/SeqFeature/Lite.pm',
    'Bio/SeqFeature/PositionProxy.pm',
    'Bio/SeqFeature/Primer.pm',
    'Bio/SeqFeature/Similarity.pm',
    'Bio/SeqFeature/SimilarityPair.pm',
    'Bio/SeqFeature/SubSeq.pm',
    'Bio/SeqFeature/Tools/FeatureNamer.pm',
    'Bio/SeqFeature/Tools/IDHandler.pm',
    'Bio/SeqFeature/Tools/TypeMapper.pm',
    'Bio/SeqFeature/Tools/Unflattener.pm',
    'Bio/SeqFeature/TypedSeqFeatureI.pm',
    'Bio/SeqFeatureI.pm',
    'Bio/SeqI.pm',
    'Bio/SeqIO.pm',
    'Bio/SeqIO/FTHelper.pm',
    'Bio/SeqIO/Handler/GenericRichSeqHandler.pm',
    'Bio/SeqIO/MultiFile.pm',
    'Bio/SeqIO/ace.pm',
    'Bio/SeqIO/asciitree.pm',
    'Bio/SeqIO/bsml.pm',
    'Bio/SeqIO/bsml_sax.pm',
    'Bio/SeqIO/embl.pm',
    'Bio/SeqIO/embldriver.pm',
    'Bio/SeqIO/fasta.pm',
    'Bio/SeqIO/fastq.pm',
    'Bio/SeqIO/game.pm',
    'Bio/SeqIO/game/featHandler.pm',
    'Bio/SeqIO/game/gameHandler.pm',
    'Bio/SeqIO/game/gameSubs.pm',
    'Bio/SeqIO/game/gameWriter.pm',
    'Bio/SeqIO/game/seqHandler.pm',
    'Bio/SeqIO/gbdriver.pm',
    'Bio/SeqIO/gbxml.pm',
    'Bio/SeqIO/gcg.pm',
    'Bio/SeqIO/genbank.pm',
    'Bio/SeqIO/kegg.pm',
    'Bio/SeqIO/largefasta.pm',
    'Bio/SeqIO/locuslink.pm',
    'Bio/SeqIO/mbsout.pm',
    'Bio/SeqIO/metafasta.pm',
    'Bio/SeqIO/msout.pm',
    'Bio/SeqIO/phd.pm',
    'Bio/SeqIO/pir.pm',
    'Bio/SeqIO/qual.pm',
    'Bio/SeqIO/raw.pm',
    'Bio/SeqIO/scf.pm',
    'Bio/SeqIO/seqxml.pm',
    'Bio/SeqIO/swiss.pm',
    'Bio/SeqIO/swissdriver.pm',
    'Bio/SeqIO/tab.pm',
    'Bio/SeqIO/table.pm',
    'Bio/SeqIO/tigr.pm',
    'Bio/SeqIO/tigrxml.pm',
    'Bio/SeqIO/tinyseq.pm',
    'Bio/SeqIO/tinyseq/tinyseqHandler.pm',
    'Bio/SeqUtils.pm',
    'Bio/SimpleAlign.pm',
    'Bio/SimpleAnalysisI.pm',
    'Bio/Species.pm',
    'Bio/Taxon.pm',
    'Bio/Tools/Alignment/Consed.pm',
    'Bio/Tools/Alignment/Trim.pm',
    'Bio/Tools/AmpliconSearch.pm',
    'Bio/Tools/Analysis/SimpleAnalysisBase.pm',
    'Bio/Tools/AnalysisResult.pm',
    'Bio/Tools/Blat.pm',
    'Bio/Tools/CodonTable.pm',
    'Bio/Tools/Coil.pm',
    'Bio/Tools/ECnumber.pm',
    'Bio/Tools/EMBOSS/Palindrome.pm',
    'Bio/Tools/EPCR.pm',
    'Bio/Tools/ESTScan.pm',
    'Bio/Tools/Eponine.pm',
    'Bio/Tools/Est2Genome.pm',
    'Bio/Tools/Fgenesh.pm',
    'Bio/Tools/FootPrinter.pm',
    'Bio/Tools/GFF.pm',
    'Bio/Tools/Geneid.pm',
    'Bio/Tools/Genemark.pm',
    'Bio/Tools/Genewise.pm',
    'Bio/Tools/Genomewise.pm',
    'Bio/Tools/Genscan.pm',
    'Bio/Tools/Glimmer.pm',
    'Bio/Tools/Grail.pm',
    'Bio/Tools/GuessSeqFormat.pm',
    'Bio/Tools/IUPAC.pm',
    'Bio/Tools/Lucy.pm',
    'Bio/Tools/MZEF.pm',
    'Bio/Tools/Match.pm',
    'Bio/Tools/OddCodes.pm',
    'Bio/Tools/Phylo/Gerp.pm',
    'Bio/Tools/Phylo/Molphy.pm',
    'Bio/Tools/Phylo/Molphy/Result.pm',
    'Bio/Tools/Phylo/Phylip/ProtDist.pm',
    'Bio/Tools/Prediction/Exon.pm',
    'Bio/Tools/Prediction/Gene.pm',
    'Bio/Tools/Primer/Assessor/Base.pm',
    'Bio/Tools/Primer/AssessorI.pm',
    'Bio/Tools/Primer/Feature.pm',
    'Bio/Tools/Primer/Pair.pm',
    'Bio/Tools/Primer3.pm',
    'Bio/Tools/Prints.pm',
    'Bio/Tools/Profile.pm',
    'Bio/Tools/Promoterwise.pm',
    'Bio/Tools/PrositeScan.pm',
    'Bio/Tools/Pseudowise.pm',
    'Bio/Tools/QRNA.pm',
    'Bio/Tools/RandomDistFunctions.pm',
    'Bio/Tools/RepeatMasker.pm',
    'Bio/Tools/Run/Analysis.pm',
    'Bio/Tools/Run/AnalysisFactory.pm',
    'Bio/Tools/Run/GenericParameters.pm',
    'Bio/Tools/Run/ParametersI.pm',
    'Bio/Tools/Run/Phylo/PhyloBase.pm',
    'Bio/Tools/Run/WrapperBase.pm',
    'Bio/Tools/Run/WrapperBase/CommandExts.pm',
    'Bio/Tools/Seg.pm',
    'Bio/Tools/SeqPattern.pm',
    'Bio/Tools/SeqPattern/Backtranslate.pm',
    'Bio/Tools/SeqStats.pm',
    'Bio/Tools/SeqWords.pm',
    'Bio/Tools/Sigcleave.pm',
    'Bio/Tools/Signalp.pm',
    'Bio/Tools/Signalp/ExtendedSignalp.pm',
    'Bio/Tools/Sim4/Exon.pm',
    'Bio/Tools/Sim4/Results.pm',
    'Bio/Tools/Spidey/Exon.pm',
    'Bio/Tools/Spidey/Results.pm',
    'Bio/Tools/TandemRepeatsFinder.pm',
    'Bio/Tools/TargetP.pm',
    'Bio/Tools/Tmhmm.pm',
    'Bio/Tools/ipcress.pm',
    'Bio/Tools/isPcr.pm',
    'Bio/Tools/pICalculator.pm',
    'Bio/Tools/tRNAscanSE.pm',
    'Bio/Tree/AnnotatableNode.pm',
    'Bio/Tree/Compatible.pm',
    'Bio/Tree/DistanceFactory.pm',
    'Bio/Tree/Node.pm',
    'Bio/Tree/NodeI.pm',
    'Bio/Tree/NodeNHX.pm',
    'Bio/Tree/RandomFactory.pm',
    'Bio/Tree/Statistics.pm',
    'Bio/Tree/Tree.pm',
    'Bio/Tree/TreeFunctionsI.pm',
    'Bio/Tree/TreeI.pm',
    'Bio/TreeIO.pm',
    'Bio/TreeIO/NewickParser.pm',
    'Bio/TreeIO/TreeEventBuilder.pm',
    'Bio/TreeIO/cluster.pm',
    'Bio/TreeIO/lintree.pm',
    'Bio/TreeIO/newick.pm',
    'Bio/TreeIO/nexus.pm',
    'Bio/TreeIO/nhx.pm',
    'Bio/TreeIO/pag.pm',
    'Bio/TreeIO/phyloxml.pm',
    'Bio/TreeIO/tabtree.pm',
    'Bio/UpdateableSeqI.pm',
    'Bio/WebAgent.pm',
    'BioPerl.pm'
);

my @scripts = (
    'bin/bp_aacomp',
    'bin/bp_bioflat_index',
    'bin/bp_biogetseq',
    'bin/bp_dbsplit',
    'bin/bp_extract_feature_seq',
    'bin/bp_fastam9_to_table',
    'bin/bp_fetch',
    'bin/bp_filter_search',
    'bin/bp_find-blast-matches',
    'bin/bp_gccalc',
    'bin/bp_genbank2gff3',
    'bin/bp_index',
    'bin/bp_local_taxonomydb_query',
    'bin/bp_make_mrna_protein',
    'bin/bp_mask_by_search',
    'bin/bp_mrtrans',
    'bin/bp_mutate',
    'bin/bp_nexus2nh',
    'bin/bp_nrdb',
    'bin/bp_oligo_count',
    'bin/bp_process_gadfly',
    'bin/bp_process_sgd',
    'bin/bp_revtrans-motif',
    'bin/bp_search2alnblocks',
    'bin/bp_search2gff',
    'bin/bp_search2table',
    'bin/bp_search2tribe',
    'bin/bp_seq_length',
    'bin/bp_seqconvert',
    'bin/bp_seqcut',
    'bin/bp_seqpart',
    'bin/bp_seqret',
    'bin/bp_seqretsplit',
    'bin/bp_split_seq',
    'bin/bp_sreformat',
    'bin/bp_taxid4species',
    'bin/bp_taxonomy2tree',
    'bin/bp_translate_seq',
    'bin/bp_tree2pag',
    'bin/bp_unflatten_seq'
);

# no fake home requested

my @switches = (
    -d 'blib' ? '-Mblib' : '-Ilib',
);

use File::Spec;
use IPC::Open3;
use IO::Handle;

open my $stdin, '<', File::Spec->devnull or die "can't open devnull: $!";

my @warnings;
for my $lib (@module_files)
{
    # see L<perlfaq8/How can I capture STDERR from an external command?>
    my $stderr = IO::Handle->new;

    diag('Running: ', join(', ', map { my $str = $_; $str =~ s/'/\\'/g; q{'} . $str . q{'} }
            $^X, @switches, '-e', "require q[$lib]"))
        if $ENV{PERL_COMPILE_TEST_DEBUG};

    my $pid = open3($stdin, '>&STDERR', $stderr, $^X, @switches, '-e', "require q[$lib]");
    binmode $stderr, ':crlf' if $^O eq 'MSWin32';
    my @_warnings = <$stderr>;
    waitpid($pid, 0);
    is($?, 0, "$lib loaded ok");

    shift @_warnings if @_warnings and $_warnings[0] =~ /^Using .*\bblib/
        and not eval { +require blib; blib->VERSION('1.01') };

    if (@_warnings)
    {
        warn @_warnings;
        push @warnings, @_warnings;
    }
}

foreach my $file (@scripts)
{ SKIP: {
    open my $fh, '<', $file or warn("Unable to open $file: $!"), next;
    my $line = <$fh>;

    close $fh and skip("$file isn't perl", 1) unless $line =~ /^#!\s*(?:\S*perl\S*)((?:\s+-\w*)*)(?:\s*#.*)?$/;
    @switches = (@switches, split(' ', $1)) if $1;

    close $fh and skip("$file uses -T; not testable with PERL5LIB", 1)
        if grep { $_ eq '-T' } @switches and $ENV{PERL5LIB};

    my $stderr = IO::Handle->new;

    diag('Running: ', join(', ', map { my $str = $_; $str =~ s/'/\\'/g; q{'} . $str . q{'} }
            $^X, @switches, '-c', $file))
        if $ENV{PERL_COMPILE_TEST_DEBUG};

    my $pid = open3($stdin, '>&STDERR', $stderr, $^X, @switches, '-c', $file);
    binmode $stderr, ':crlf' if $^O eq 'MSWin32';
    my @_warnings = <$stderr>;
    waitpid($pid, 0);
    is($?, 0, "$file compiled ok");

    shift @_warnings if @_warnings and $_warnings[0] =~ /^Using .*\bblib/
        and not eval { +require blib; blib->VERSION('1.01') };

    # in older perls, -c output is simply the file portion of the path being tested
    if (@_warnings = grep { !/\bsyntax OK$/ }
        grep { chomp; $_ ne (File::Spec->splitpath($file))[2] } @_warnings)
    {
        warn @_warnings;
        push @warnings, @_warnings;
    }
} }



is(scalar(@warnings), 0, 'no warnings found')
    or diag 'got warnings: ', ( Test::More->can('explain') ? Test::More::explain(\@warnings) : join("\n", '', @warnings) ) if $ENV{AUTHOR_TESTING};


