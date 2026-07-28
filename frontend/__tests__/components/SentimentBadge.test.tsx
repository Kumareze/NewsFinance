/**
 * Tests for SentimentBadge component
 */

import React from "react";
import { render, screen } from "@testing-library/react";
import SentimentBadge from "@/components/SentimentBadge";

describe("SentimentBadge", () => {
  it("renders positive sentiment correctly", () => {
    render(<SentimentBadge sentiment="positive" />);
    expect(screen.getByText("Positive")).toBeInTheDocument();
  });

  it("renders negative sentiment correctly", () => {
    render(<SentimentBadge sentiment="negative" />);
    expect(screen.getByText("Negative")).toBeInTheDocument();
  });

  it("renders neutral sentiment correctly", () => {
    render(<SentimentBadge sentiment="neutral" />);
    expect(screen.getByText("Neutral")).toBeInTheDocument();
  });

  it("displays confidence percentage when provided", () => {
    render(<SentimentBadge sentiment="positive" confidence={0.85} />);
    expect(screen.getByText(/85%/)).toBeInTheDocument();
  });

  it("does not display confidence when not provided", () => {
    render(<SentimentBadge sentiment="positive" />);
    expect(screen.queryByText(/%/)).not.toBeInTheDocument();
  });
});
