# Migration Notes

## Early Recovery

This repository contains one of the earliest recovered components from the Navigation Network.

The original implementation included a migration path from legacy station snapshots. The later Reverse Mountain team carried forward the migration effort after the Restoration Division encountered compatibility drift during initial rebuilds.

## Known Issues

- The entry point preserves a transition artifact from the earliest recovered service.
- There is no local snapshot validation for `legacy-stations.yml` beyond the migration deserializer.
- Some module references in the root package reflect an older service structure.
