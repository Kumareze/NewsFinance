/**
 * Tests for Pagination component
 */

import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import Pagination from "@/components/Pagination";

describe("Pagination", () => {
  it("renders nothing when there is only one page", () => {
    const { container } = render(
      <Pagination label="Positive News" page={1} totalPages={1} onChange={jest.fn()} />
    );
    expect(container).toBeEmptyDOMElement();
  });

  it("shows current page and total pages", () => {
    render(<Pagination label="Positive News" page={2} totalPages={5} onChange={jest.fn()} />);
    expect(screen.getByText("Halaman 2 dari 5")).toBeInTheDocument();
  });

  it("calls onChange with the previous page", () => {
    const onChange = jest.fn();
    render(<Pagination label="Positive News" page={3} totalPages={5} onChange={onChange} />);
    fireEvent.click(screen.getByRole("button", { name: /sebelumnya/i }));
    expect(onChange).toHaveBeenCalledWith(2);
  });

  it("calls onChange with the next page", () => {
    const onChange = jest.fn();
    render(<Pagination label="Positive News" page={1} totalPages={5} onChange={onChange} />);
    fireEvent.click(screen.getByRole("button", { name: /berikutnya/i }));
    expect(onChange).toHaveBeenCalledWith(2);
  });

  it("disables previous on the first page and next on the last page", () => {
    const { rerender } = render(
      <Pagination label="Positive News" page={1} totalPages={3} onChange={jest.fn()} />
    );
    expect(screen.getByRole("button", { name: /sebelumnya/i })).toBeDisabled();

    rerender(<Pagination label="Positive News" page={3} totalPages={3} onChange={jest.fn()} />);
    expect(screen.getByRole("button", { name: /berikutnya/i })).toBeDisabled();
  });

  it("exposes an accessible name per section", () => {
    render(<Pagination label="Negative News" page={1} totalPages={2} onChange={jest.fn()} />);
    expect(screen.getByRole("navigation", { name: "Halaman Negative News" })).toBeInTheDocument();
  });
});
