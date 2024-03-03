import React from 'react';
import { useLocation } from 'react-router-dom';

const ConfirmationPage: React.FC = () => {
    const location = useLocation();
    const { orderStatusResponse } = location.state as any;

    // Convert verification status to a readable format
    const verificationStatus = orderStatusResponse.verification === 'True' ? 'Success' : 'Failed';

    return (
        <div className="container mt-5">
            <h1>Order Status: {verificationStatus}</h1>
            {orderStatusResponse.orderId && <h2>Order ID: {orderStatusResponse.orderId}</h2>}
            {orderStatusResponse.status && <p>Status: {orderStatusResponse.status}</p>}
            {verificationStatus === 'Failed' && orderStatusResponse.errors && orderStatusResponse.errors.length > 0 &&
                <div>
                    <h3>Verification Errors:</h3>
                    <ul>
                        {orderStatusResponse.errors.map((error: string, index: number) => (
                            <li key={index}>{error}</li>
                        ))}
                    </ul>
                </div>
            }
            {orderStatusResponse.suggestedBooks && orderStatusResponse.suggestedBooks.length > 0 &&
                <div>
                    <h3>Suggested Books</h3>
                    <ul>
                        {orderStatusResponse.suggestedBooks.map((book: any, index: number) => (
                            <li key={index}>
                                <h4>{book.title}</h4>
                                <p>Book ID: {book.bookId}<br />
                                Author: {book.author}</p>
                            </li>
                        ))}
                    </ul>
                </div>
            }
        </div>
    );
};

export default ConfirmationPage;
