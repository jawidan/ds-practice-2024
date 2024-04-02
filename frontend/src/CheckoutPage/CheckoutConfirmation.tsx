import React from 'react';
import { useLocation } from 'react-router-dom';

const ConfirmationPage: React.FC = () => {
    const location = useLocation();
    const { orderStatusResponse } = location.state as any;

    // Determine status and fraud detection
    const status = orderStatusResponse.verification === 'True' ? 'Order Verified' : 'Order Failed';
    const isFraudulent = orderStatusResponse.isFraudulent;

    return (
        <div className="container mt-5">
            <div className="card">
                <div className="card-body">
                    <h2 className="card-title">Order Status</h2>
                    <p className={`status ${orderStatusResponse.verification.toLowerCase()}`}>{status}</p>
                    {orderStatusResponse.verification === 'False' && (
                        <div>
                            <h3>Errors:</h3>
                            <ul className="error-list">
                                {orderStatusResponse.errors.map((error: string, index: number) => (
                                    <li key={index} className="error-item">{error}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {orderStatusResponse.verification === 'True' && (
                        <div>
                            <h3>Order ID: <span className="order-id">{orderStatusResponse.orderID}</span></h3>
                            <h3>Order Status: <span className="order-status">{orderStatusResponse.orderStatus}</span></h3>
                            {orderStatusResponse.suggestedBooks && orderStatusResponse.suggestedBooks.length > 0 && (
                                <div>
                                    <h3>Suggested Books For Your Order:</h3>
                                    <ul className="suggested-books">
                                        {orderStatusResponse.suggestedBooks.map((book: any, index: number) => (
                                            <li key={index} className="suggested-book">
                                                <p>{book.title}</p>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                    {/* Optionally display fraud reason */}
                    {/* {isFraudulent && (
                        <div>
                            <h3>Fraud Reason:</h3>
                            <p>{orderStatusResponse.fraudReason}</p>
                        </div>
                    )} */}
                </div>
            </div>
        </div>
    );
};

export default ConfirmationPage;