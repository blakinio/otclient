# ADR-0002: Data-Oriented Runtime and wgpu Renderer

Status: accepted  
Date: 2026-07-26

## Context

The client must support dense 2D world scenes, high-refresh presentation, large UI surfaces and predictable frame time. A direct object-oriented port would preserve scattered allocations and renderer coupling.

## Decision

Use data-oriented storage for hot game state, including specialized arenas/sparse sets, struct-of-arrays where beneficial and chunked world storage.

Use `wgpu` as the primary GPU abstraction. Rendering consumes extracted snapshots and uses instancing, batching, cached pipelines/resources and asynchronous asset upload.

Do not select a general-purpose game engine or reflection-heavy universal ECS as the product foundation. Individual supporting libraries remain subject to the audit and dependency review.

## Consequences

- domain/simulation and renderer have a strict snapshot boundary;
- performance-critical memory layout remains under project control;
- one renderer can target modern Windows GPU APIs while retaining future portability;
- more engine/UI infrastructure must be developed and benchmarked by the project.

## Rejected

- OpenGL as the primary new backend;
- renderer reading mutable game objects directly;
- one heap object per visible thing as the default model;
- per-sprite script callbacks;
- selecting Vulkan/D3D12 directly before portability and maintenance evidence requires it.
