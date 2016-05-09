#############################
# This cfg configures the part of reconstruction 
# in FastSim to be done before event mixing
# FastSim mixes tracker information on reconstruction level,
# so tracks are recontructed before mixing.
# At present, only the generalTrack collection, produced with iterative tracking is mixed.
#############################

import FWCore.ParameterSet.Config as cms


# iterative tracking relies on the beamspot
from RecoVertex.BeamSpotProducer.BeamSpot_cff import offlineBeamSpot

# and of course it needs tracker hits
from FastSimulation.TrackingRecHitProducer.SiTrackerGaussianSmearingRecHitConverter_cfi import siTrackerGaussianSmearingRecHits
#from FastSimulation.TrackingRecHitProducer.NewRecHitConverter_NoMerge_cfi import trackingRecHitProducerNoMerge as siTrackerGaussianSmearingRecHits
#from FastSimulation.TrackingRecHitProducer.NewRecHitConverter_Example_cfi import trackingRecHitProducer as siTrackerGaussianSmearingRecHits
#from FastSimulation.TrackingRecHitProducer.NewRecHitConverter_Example_cfi import trackingRecHitProducer_alt as siTrackerGaussianSmearingRecHits

recHitResolutionPixels = cms.EDProducer("RecHitResolution",
    hitSrc=cms.InputTag("siTrackerGaussianSmearingRecHits"),
    hitCombinationSrc=cms.InputTag("siTrackerGaussianSmearingRecHits","simHit2RecHitMap"),
    nbinsSmearing = cms.int32(200),
    xminSmearing = cms.double(-0.05),
    xmaxSmearing = cms.double(0.05),
    yminSmearing = cms.double(-0.05),
    ymaxSmearing = cms.double(0.05),
    
    nbinsError = cms.int32(200),
    xminError = cms.double(0.0),
    xmaxError = cms.double(0.005),
    yminError = cms.double(0.0),
    ymaxError = cms.double(0.006),
    select = cms.string("subdetId == BPX || subdetId == FPX")
)

recHitResolutionTOB = cms.EDProducer("RecHitResolution",
    hitSrc=cms.InputTag("siTrackerGaussianSmearingRecHits"),
    hitCombinationSrc=cms.InputTag("siTrackerGaussianSmearingRecHits","simHit2RecHitMap"),
    nbinsSmearing = cms.int32(200),
    xminSmearing = cms.double(-0.05),
    xmaxSmearing = cms.double(0.05),
    yminSmearing = cms.double(-0.5),
    ymaxSmearing = cms.double(0.5),
    
    nbinsError = cms.int32(200),
    xminError = cms.double(0.0025),
    xmaxError = cms.double(0.005),
    yminError = cms.double(5.0),
    ymaxError = cms.double(5.4),
    select = cms.string("subdetId==TOB")
)

recHitResolutionTID = cms.EDProducer("RecHitResolution",
    hitSrc=cms.InputTag("siTrackerGaussianSmearingRecHits"),
    hitCombinationSrc=cms.InputTag("siTrackerGaussianSmearingRecHits","simHit2RecHitMap"),
    nbinsSmearing = cms.int32(200),
    xminSmearing = cms.double(-0.05),
    xmaxSmearing = cms.double(0.05),
    yminSmearing = cms.double(-0.5),
    ymaxSmearing = cms.double(0.5),
    
    nbinsError = cms.int32(200),
    xminError = cms.double(0.0),
    xmaxError = cms.double(0.005),
    yminError = cms.double(3.3),
    ymaxError = cms.double(3.5),
    select = cms.string("subdetId==TID")
)


recHitResolutionOther = cms.EDProducer("RecHitResolution",
    hitSrc=cms.InputTag("siTrackerGaussianSmearingRecHits"),
    hitCombinationSrc=cms.InputTag("siTrackerGaussianSmearingRecHits","simHit2RecHitMap"),
    nbinsSmearing = cms.int32(200),
    xminSmearing = cms.double(-0.05),
    xmaxSmearing = cms.double(0.05),
    yminSmearing = cms.double(-0.5),
    ymaxSmearing = cms.double(0.5),
    
    nbinsError = cms.int32(200),
    xminError = cms.double(0.0),
    xmaxError = cms.double(0.01),
    yminError = cms.double(3.3),
    ymaxError = cms.double(3.8),
    select = cms.string("subdetId==TIB || subdetId==TEC")
)


from FastSimulation.TrackingRecHitProducer.FastTrackerRecHitMatcher_cfi import fastMatchedTrackerRecHits
import FastSimulation.Tracking.FastTrackerRecHitCombiner_cfi

fastMatchedTrackerRecHitCombinations = FastSimulation.Tracking.FastTrackerRecHitCombiner_cfi.fastTrackerRecHitCombinations.clone(
    simHit2RecHitMap = cms.InputTag("fastMatchedTrackerRecHits","simHit2RecHitMap")
    )

# FastSim stores the IdealMagneticFieldRecord and the TrackerInteractionGeometryRecord in a particular structure
# This extra layer is probably more confusing than it is useful and we should consider to remove it
from FastSimulation.ParticlePropagator.MagneticFieldMapESProducer_cfi import *

# confusing name for the file that imports 
# the fitters used by the TrackProducer
# 
from TrackingTools.MaterialEffects.Propagators_cff import *
from TrackingTools.TrackFitters.TrackFitters_cff import *
from RecoTracker.TransientTrackingRecHit.TransientTrackingRecHitBuilderWithoutRefit_cfi import *
from TrackingTools.KalmanUpdators.KFUpdatorESProducer_cfi import *
from TrackingTools.KalmanUpdators.Chi2MeasurementEstimator_cfi import *

#  MeasurementTrackerEvent
from RecoLocalTracker.SiPixelRecHits.PixelCPEGeneric_cfi import *
from RecoTracker.MeasurementDet.MeasurementTrackerESProducer_cff import *
from FastSimulation.Tracking.MeasurementTrackerEventProducer_cfi import MeasurementTrackerEvent
# services needed by tracking
from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import TransientTrackBuilderESProducer
from RecoTracker.TkNavigation.NavigationSchoolESProducer_cfi import navigationSchoolESProducer

from FastSimulation.Tracking.iterativeTk_cff import *
from TrackingTools.TrackFitters.TrackFitters_cff import *

reconstruction_befmix = cms.Sequence(
    offlineBeamSpot
    * siTrackerGaussianSmearingRecHits
    * recHitResolutionPixels
    * recHitResolutionTOB
    * recHitResolutionTID
    * recHitResolutionOther
    * fastMatchedTrackerRecHits
    * fastMatchedTrackerRecHitCombinations
    * MeasurementTrackerEvent
    * iterTracking
    )
